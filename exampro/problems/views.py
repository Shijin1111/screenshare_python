from django.shortcuts import render, get_object_or_404
from .models import Problem,TestCase
import subprocess

def home(request):
    problems = Problem.objects.all()
    return render(request, 'problems/home.html', {'problems': problems})

def problem_details(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    output = ""
    success = False
    test_case = None

    if request.method == 'POST':
        language = request.POST['language']
        code = request.POST['code']
        
        # Fetch the first test case for demonstration (modify as needed)
        test_case = problem.test_cases.first()
        
        if test_case:
            user_input = test_case.input_data
            expected_output = test_case.expected_output

            # Prepare execution environment based on language
            try:
                if language == 'python':
                    process = subprocess.run(
                        ['python3', '-c', code],
                        input=user_input.encode(),
                        capture_output=True,
                        timeout=5
                    )
                    output = process.stdout.decode().strip()
                elif language == 'cpp':
                    # Similar logic for compiling/running C++ code
                    output = "C++ execution logic not implemented here."
                elif language == 'java':
                    # Similar logic for compiling/running Java code
                    output = "Java execution logic not implemented here."
            except subprocess.TimeoutExpired:
                output = "Execution timed out."

            # Check for success/failure
            success = (output == expected_output)

    return render(request, 'problems/problem_details.html', {
        'problem': problem,
        'output': output,
        'success': success,
        'test_case': test_case
    })