from django.shortcuts import render, get_object_or_404
from .models import Problem,TestCase
import subprocess,os

def home(request):
    problems = Problem.objects.all()
    return render(request, 'problems/home.html', {'problems': problems})



def problem_details(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    results = []
    code = ""
    language = "python"

    if request.method == 'POST':
        language = request.POST.get('language')
        code = request.POST.get('code')

        test_cases = problem.test_cases.all()
        
        for test_case in test_cases:
            user_input = test_case.input_data.strip()
            expected_output = test_case.expected_output.strip()
            output = ""
            success = False

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
                    with open('code.cpp', 'w') as f:
                        f.write(code)

                    # Compile C++ code
                    compile_process = subprocess.run(['g++', 'code.cpp', '-o', 'code.out'], capture_output=True)
                    if compile_process.returncode != 0:
                        output = compile_process.stderr.decode().strip()
                    else:
                        # Execute the compiled C++ binary
                        process = subprocess.run(['./code.out'], input=user_input.encode(), capture_output=True, timeout=5)
                        output = process.stdout.decode().strip()

                elif language == 'java':
                    with open('Main.java', 'w') as f:
                        f.write(code)

                    # Compile Java code
                    compile_process = subprocess.run(['javac', 'Main.java'], capture_output=True)
                    if compile_process.returncode != 0:
                        output = compile_process.stderr.decode().strip()
                    else:
                        # Execute the compiled Java class
                        process = subprocess.run(['java', 'Main'], input=user_input.encode(), capture_output=True, timeout=5)
                        output = process.stdout.decode().strip()

            except subprocess.TimeoutExpired:
                output = "Execution timed out."

            success = (output == expected_output)
            results.append({
                'test_case': test_case,
                'output': output,
                'expected_output': expected_output,
                'success': success
            })

        # Clean up temporary files
        for filename in ['code.cpp', 'code.out', 'Main.java', 'Main.class']:
            if os.path.exists(filename):
                os.remove(filename)

    return render(request, 'problems/problem_details.html', {
        'problem': problem,
        'results': results,
        'code': code,
        'language': language
    })
