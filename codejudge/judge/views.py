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
                cmd = f"python3 /code/script.py"

            elif language == "c":
                file_path = f"{temp_dir}/program.c"
                cmd = f"gcc /code/program.c -o /code/program.out && /code/program.out"

            elif language == "cpp":
                file_path = f"{temp_dir}/program.cpp"
                cmd = f"g++ /code/program.cpp -o /code/program.out && /code/program.out"

            elif language == "java":
                file_path = f"{temp_dir}/Main.java"
                cmd = f"javac /code/Main.java && java -cp /code Main"

            else:
                return JsonResponse({"error": "Unsupported language"}, status=400)

            # Write the user's code to a file
            with open(file_path, "w") as code_file:
                code_file.write(code)

            # Run the code inside Docker (isolated environment)
            docker_cmd = f"docker exec code-executor bash -c 'echo \"{code}\" > {file_path} && {cmd}'"
            result = subprocess.run(docker_cmd, shell=True, text=True, capture_output=True, timeout=5)

            return JsonResponse({"output": result.stdout, "error": result.stderr, "status": "Success"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)
