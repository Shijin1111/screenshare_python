# import os
# import subprocess
# import json
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def execute_code(request):
#     if request.method == "GET":
#         return render(request, "judge/execute.html")

#     elif request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             language = data.get("language")
#             code = data.get("code")
#             input_data = data.get("input_data", "")

#             if not language or not code:
#                 return JsonResponse({"error": "Missing language or code"}, status=400)

#             # Set the correct path inside the container
#             temp_dir = "C:/Users/shiji/Desktop/cnew/screenshare/codejudge/temp_code"  # Local path that maps to /code in Docker

#             # Ensure the directory exists on the host (not the container)
#             if not os.path.exists(temp_dir):
#                 os.makedirs(temp_dir)
#                 print(f"Directory {temp_dir} created")

#             # Choose file paths based on language
#             if language == "python":
#                 file_path = f"{temp_dir}/script.py"
#                 cmd = f"python3 /code/script.py"

#             elif language == "c":
#                 file_path = f"{temp_dir}/program.c"
#                 cmd = f"gcc /code/program.c -o /code/program.out && /code/program.out"

#             elif language == "cpp":
#                 file_path = f"{temp_dir}/program.cpp"
#                 cmd = f"g++ /code/program.cpp -o /code/program.out && /code/program.out"

#             elif language == "java":
#                 file_path = f"{temp_dir}/Main.java"
#                 cmd = f"javac /code/Main.java && java -cp /code Main"

#             else:
#                 return JsonResponse({"error": "Unsupported language"}, status=400)

#             # Debugging: Print file path and code before writing
#             print(f"Writing code to {file_path}: {code}")  # This will show the code you're writing
#             print(f"Writing to file : {file_path}")  # Debugging

#             # Write the user's code to a file
#             with open(file_path, "w") as code_file:
#                 print(f"Writing code to {file_path}: {code}")  # Debugging line
#                 code_file.write(code)
#                 code_file.flush()  # Flush internal buffer
#                 os.fsync(code_file.fileno())

#             # Check if the file content was written properly
#             with open(file_path, "r") as code_file:
#                 content = code_file.read()
#                 print(f"File content after writing: {content}")  # Debugging line

#             # Run the code inside Docker
#             container_name = "new-code-executor"  # Replace this with the actual container name
#             docker_cmd = f"echo '{input_data}' | docker run --rm -v C:/Users/shiji/Desktop/cnew/screenshare/codejudge/temp_code:/code {container_name} bash -c \"python3 /code/script.py\""

#             print(f"Running command: {docker_cmd}")  # Debug the Docker command
#             result = subprocess.run(docker_cmd, shell=True, text=True, capture_output=True, timeout=15)

#             # Return all captured output, including stdout, stderr, and return code
#             return JsonResponse({
#                 "output": result.stdout,
#                 "error": result.stderr,
#                 "status": "Success",
#                 "returncode": result.returncode
#             })

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Only POST requests are allowed"}, status=400)


from django.shortcuts import render, get_object_or_404
from .models import Question, Submission, TestCase
from .utils import execute_code

def submit_code(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    status = None
    selected_language = "python"  # Default language
    error_details = None  # To store error messages
    test_case_results = []
    code = ""

    if request.method == "POST":
        code = request.POST.get("code")
        selected_language = request.POST.get("language")  # Store selected language

        test_cases = TestCase.objects.filter(question=question)
        all_passed = True

        for test in test_cases:
            result = execute_code(code, selected_language, test.input_data)

            # Check if the result matches the expected output
            if result.strip() != test.expected_output.strip():
                all_passed = False
                test_case_results.append({
                    "input": test.input_data,
                    "expected": test.expected_output,
                    "result": result,
                    "status": "Failed"
                })
            else:
                test_case_results.append({
                    "input": test.input_data,
                    "expected": test.expected_output,
                    "result": result,
                    "status": "Passed"
                })

        status = "Accepted" if all_passed else "Wrong Answer"
        Submission.objects.create(user="TestUser", question=question, code=code, language=selected_language, status=status)

        # If any error occurs during code execution, store that as well
        error_details = "Check the output below for errors" if not all_passed else None

    return render(request, "judge/submit.html", {
        "question": question,
        "status": status,
        "language": selected_language,
        "code": code,
        "test_case_results": test_case_results,
        "error_details": error_details
    })




def home(request):
    questions = Question.objects.all()
    return render(request, "judge/home.html", {"questions": questions})
