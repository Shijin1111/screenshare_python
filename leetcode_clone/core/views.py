from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Problem, Submission, Leaderboard
from django.contrib.auth.decorators import login_required

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'core/problem_list.html', {'problems': problems})

import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Problem, TestCase

import json
import subprocess
import tempfile
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Problem

@csrf_exempt
def problem_detail(request, problem_id):
    problem = Problem.objects.get(id=problem_id)

    if request.method == "POST":
        try:
            code = request.POST.get('code', '')
            language = request.POST.get('language', '')

            if not code or not language:
                return JsonResponse({"error": "Code or language missing"}, status=400)

            test_cases = problem.test_cases.all()
            prefix = getattr(problem, f"prefix_{language}", "")
            main_code = getattr(problem, f"main_{language}", "")
            final_code = generate_final_code(prefix, code, main_code, language)

            results = run_code(final_code, language, test_cases)
            
            return JsonResponse({"results": results})

        except Exception as e:
            import traceback
            print("Error in problem_detail:", traceback.format_exc())  # Log to console
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, 'core/problem_detail.html', {
        'problem': problem,
        'python_signature': problem.python_signature,
        'cpp_signature': problem.cpp_signature,
        'java_signature': problem.java_signature,
    })

import subprocess
import json
import tempfile
import os
import tempfile
import os
import subprocess
import json

def run_code(code, language, test_cases):
    print("Executing run_code function...")
    results = []

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{language}") as temp_file:
        temp_file.write(code.encode())
        temp_file.close()

        print(f"Temp file created: {temp_file.name}")

        if language == "python":
            command = f"python3 {temp_file.name}"
        elif language == "cpp":
            compile_command = f"g++ {temp_file.name} -o {temp_file.name}.out"
            subprocess.run(compile_command, shell=True, capture_output=True)
            command = f"{temp_file.name}.out"
        elif language == "java":
            compile_command = f"javac {temp_file.name}"
            subprocess.run(compile_command, shell=True, capture_output=True)
            command = f"java {temp_file.name.replace('.java', '')}"
        else:
            print("Unsupported language!")
            return []

        print(f"Command to execute: {command}")

        for test_case in test_cases:
            input_data = json.dumps(test_case.input_data)
            expected_output = test_case.expected_output
            print(f"Running test case: {input_data}")

            try:
                process = subprocess.run(command, input=input_data, text=True, capture_output=True, timeout=5, shell=True)
                actual_output = process.stdout.strip()
                error_output = process.stderr.strip()

                print(f"Test Output: {actual_output}")  
                print(f"Expected Output: {expected_output}")

                if error_output:
                    print(f"Error Output: {error_output}")  # Debugging

                # Convert actual output to JSON (if possible)
                try:
                    actual_output_json = json.loads(actual_output)
                except json.JSONDecodeError:
                    actual_output_json = actual_output  # Keep it as a string if it's not valid JSON

                # Compare JSON outputs instead of raw strings
                status = "Pass" if json.loads(actual_output) == expected_output else "Fail"

                results.append({
                    "input": input_data,
                    "expected": expected_output,
                    "actual": actual_output_json,
                    "status": status
                })

            except subprocess.TimeoutExpired:
                print("Test case timed out!")
                results.append({"status": "Timeout"})
            except Exception as e:
                print(f"Execution error: {e}")
                results.append({"status": "Execution Error"})

        os.remove(temp_file.name)
        print("Execution completed.")

    return results

def generate_final_code(prefix, user_code, main_code, language):
    """
    Generate the final code by combining the prefix, user code, and main code.
    Ensure consistent indentation for user code based on language.
    """
    if language in {"cpp", "java"}:
        # For C++ and Java, ensure proper indentation with curly braces if needed
        user_code = '\n'.join([f"    {line}" for line in user_code.splitlines()])

    # Combine the code parts without modifying Python indentation
    final_code = f"{prefix}\n\n{user_code}\n\n{main_code}"
    print(final_code)
    return final_code
