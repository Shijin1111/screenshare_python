# core/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Problem, Submission, Leaderboard
from django.contrib.auth.decorators import login_required

# View to display all problems
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'core/problem_list.html', {'problems': problems})

# View to display details of a problem
def problem_detail(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    return render(request, 'core/problem_detail.html', {'problem': problem})

from .utils import evaluate_code

@login_required
def submit_solution(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']

        # Store the submission
        submission = Submission.objects.create(
            user=request.user,
            problem_id=problem_id,
            code=code,
            language=language,
            result="pending"
        )

        # Evaluate the code based on the selected language
        result = evaluate_code(code, language, problem_id)

        # Update the submission result
        submission.result = result
        submission.save()

        return redirect('core:problem_list')

    return render(request, 'core/submit_solution.html', {
        'problem': problem,
        'python_signature': problem.python_signature,
        'cpp_signature': problem.cpp_signature,
        'java_signature': problem.java_signature,
    })

def generate_final_code(prefix, user_code, main_code, language):
    """
    Generate the final code by combining the prefix, user code, and main code.
    Ensure proper indentation for user code based on language.
    """
    if language == "python":
        # For Python, user code should be indented with 4 spaces
        user_code = '\n'.join([f"    {line}" for line in user_code.splitlines()])
    elif language == "cpp" or language == "java":
        # For C++ and Java, ensure proper indentation with curly braces, for example
        user_code = '\n'.join([f"    {line}" for line in user_code.splitlines()])

    # Combine the code parts
    final_code = f"{prefix}\n\n{user_code}\n\n{main_code}"
    
    return final_code

import subprocess
import tempfile
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Problem

def run_code(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == "POST":
        language = request.POST.get("language")
        user_code = request.POST.get("code", "").strip()

        # Fetch prefix and main code based on selected language
        if language == "python":
            prefix = problem.prefix_python
            main_code = problem.main_python
            filename = "solution.py"
            command = ["python", filename]  # Changed to use python on Windows
        elif language == "cpp":
            prefix = problem.prefix_cpp
            main_code = problem.main_cpp
            filename = "solution.cpp"
            command = ["g++", filename, "-o", "solution", "&&", "./solution"]
        elif language == "java":
            prefix = problem.prefix_java
            main_code = problem.main_java
            filename = "Solution.java"
            command = ["javac", filename, "&&", "java", "Solution"]
        else:
            return JsonResponse({"error": "Invalid language selected"}, status=400)

        final_code = generate_final_code(prefix, user_code, main_code, language)

        try:
            # Use tempfile to generate a temporary filename
            temp_dir = tempfile.gettempdir()  # Get the system's temp directory
            file_path = os.path.join(temp_dir, filename)

            with open(file_path, "w") as f:
                f.write(final_code)
        except Exception as e:
            return JsonResponse({"error": f"Error saving code to file: {str(e)}"}, status=500)

        try:
            # Ensure that we are using the correct directory path for subprocess to find the file
            if os.path.exists(file_path):
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    cwd=temp_dir,  # Set the current working directory to the temp directory
                    timeout=5  # Prevent infinite loops
                )
                output = result.stdout if result.returncode == 0 else result.stderr
            else:
                return JsonResponse({"error": f"File not found: {file_path}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Error running code: {str(e)}"}, status=500)

        return JsonResponse({"output": output})

    return JsonResponse({"error": "Invalid request method"}, status=400)
