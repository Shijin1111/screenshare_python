from django.shortcuts import render, get_object_or_404
from .models import Problem
import subprocess

def home(request):
    problems = Problem.objects.all()
    return render(request, 'problems/home.html', {'problems': problems})


def problem_details(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    code = ""
    language = "python"
    output = None

    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")

        file_map = {
            "python": "solution.py",
            "cpp": "solution.cpp",
            "java": "Solution.java"
        }

        try:
            # Write code to a file
            with open(file_map[language], "w") as file:
                file.write(code)

            if language == "cpp":
                compile_process = subprocess.run(["g++", file_map["cpp"], "-o", "solution.out"], capture_output=True, text=True)
                if compile_process.returncode != 0:
                    output = compile_process.stderr
                else:
                    execution = subprocess.run(["./solution.out"], capture_output=True, text=True)
                    output = execution.stdout if execution.returncode == 0 else execution.stderr
            elif language == "java":
                compile_process = subprocess.run(["javac", file_map["java"]], capture_output=True, text=True)
                if compile_process.returncode != 0:
                    output = compile_process.stderr
                else:
                    execution = subprocess.run(["java", "Solution"], capture_output=True, text=True)
                    output = execution.stdout if execution.returncode == 0 else execution.stderr
            else:  # Python
                execution = subprocess.run(["python3", file_map["python"]], capture_output=True, text=True)
                output = execution.stdout if execution.returncode == 0 else execution.stderr

        except Exception as e:
            output = f"Error: {str(e)}"

    return render(request, 'problems/problem_details.html', {
        'problem': problem,
        'code': code,
        'language': language,
        'output': output
    })
