from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import io

@csrf_exempt
def execute_code(request):
    if request.method == "GET":
        return render(request, "judge/execute.html")  # Render the web page

    elif request.method == "POST":
        try:
            data = json.loads(request.body)  # Read JSON data
            language = data.get("language")
            code = data.get("code")
            input_data = data.get("input_data", "")

            if not language or not code:
                return JsonResponse({"error": "Missing language or code"}, status=400)

            if language != "python":
                return JsonResponse({"error": "Only Python is supported"}, status=400)

            # Capture stdout and stdin
            old_stdout = sys.stdout
            old_stdin = sys.stdin
            sys.stdout = new_stdout = io.StringIO()
            sys.stdin = io.StringIO(input_data)  # Redirect input

            try:
                exec(code)  # Execute user-submitted code
            except Exception as e:
                sys.stdout = old_stdout
                sys.stdin = old_stdin
                return JsonResponse({"error": str(e)}, status=500)

            # Get output and restore stdout/stdin
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
            sys.stdin = old_stdin

            return JsonResponse({"output": output, "status": "Success"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)
