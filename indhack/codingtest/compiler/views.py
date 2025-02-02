import requests
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt

# Logger for debugging
logger = logging.getLogger(__name__)

JUDGE0_API_URL = "https://judge0.p.rapidapi.com/submissions"
HEADERS = {
    "X-RapidAPI-Key": "67d1431097msh052cbe13affa107p1a6de0jsn7d0929e843c5",  # Make sure to replace with your API key
    "X-RapidAPI-Host": "judge0.p.rapidapi.com"
}
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

@csrf_exempt  # Allows POST requests from JavaScript
def run_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            language_id = data.get("language_id", "")
            input_data = data.get("input_data", "")

            if not code or not language_id:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            # API request to online compiler (JDoodle, Piston, etc.)
            API_URL = "https://api.jdoodle.com/v1/execute"
            API_CLIENT_ID = "your_client_id"
            API_CLIENT_SECRET = "your_client_secret"

            payload = {
                "script": code,
                "language": language_id,
                "stdin": input_data,
                "versionIndex": "0",
                "clientId": API_CLIENT_ID,
                "clientSecret": API_CLIENT_SECRET
            }

            response = requests.post(API_URL, json=payload)
            return JsonResponse(response.json())

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)  # Return 405 for GET requests
