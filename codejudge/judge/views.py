from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import os

@csrf_exempt
def execute_code(request):
    if request.method == "GET":
        return render(request, "judge/execute.html")

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            language = data.get("language")
            code = data.get("code")
            input_data = data.get("input_data", "")

            if not language or not code:
                return JsonResponse({"error": "Missing language or code"}, status=400)

            temp_dir = "temp_code"
            os.makedirs(temp_dir, exist_ok=True)

            if language == "python":
                file_path = f"{temp_dir}/script.py"
                cmd = ["python3", file_path]

            elif language == "c":
                file_path = f"{temp_dir}/program.c"
                executable = f"{temp_dir}/program.out"
                cmd = ["gcc", file_path, "-o", executable]
                run_cmd = [executable]

            elif language == "cpp":
                file_path = f"{temp_dir}/program.cpp"
                executable = f"{temp_dir}/program.out"
                cmd = ["g++", file_path, "-o", executable]
                run_cmd = [executable]

            elif language == "java":
                file_path = f"{temp_dir}/Main.java"
                cmd = ["javac", file_path]
                run_cmd = ["java", "-cp", temp_dir, "Main"]

            else:
                return JsonResponse({"error": "Unsupported language"}, status=400)

            # Write the user's code to a file
            with open(file_path, "w") as code_file:
                code_file.write(code)

            if language in ["python"]:
                result = subprocess.run(cmd, input=input_data, text=True, capture_output=True, timeout=5)
            else:
                compile_result = subprocess.run(cmd, capture_output=True, text=True)

                if compile_result.returncode != 0:
                    return JsonResponse({"error": compile_result.stderr}, status=400)

                result = subprocess.run(run_cmd, input=input_data, text=True, capture_output=True, timeout=5)

            return JsonResponse({"output": result.stdout, "error": result.stderr, "status": "Success"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)
