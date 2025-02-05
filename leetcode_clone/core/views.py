from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Problem, Submission, Leaderboard
from django.contrib.auth.decorators import login_required

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'core/problem_list.html', {'problems': problems})

def problem_detail(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']
        
        submission = Submission.objects.create(
            user=request.user,
            problem_id=problem_id,
            code=code,
            language=language,
            result="pending"
        )
        
    return render(request, 'core/problem_detail.html', {
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
