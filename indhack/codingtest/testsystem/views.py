from django.shortcuts import render
from django.http import JsonResponse
from .models import Question, TestCase
import requests

JUDGE0_API_URL = "https://judge0.p.rapidapi.com/submissions"
HEADERS = {
    "X-RapidAPI-Key": "67d1431097msh052cbe13affa107p1a6de0jsn7d0929e843c5",
    "X-RapidAPI-Host": "judge0.p.rapidapi.com"
}

def coding_test(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, "testsystem/coding_test.html", {"question": question})

def submit_code(request, question_id):
    if request.method == "POST":
        code = request.POST.get("code")
        language_id = request.POST.get("language_id")
        question = Question.objects.get(id=question_id)
        test_cases = TestCase.objects.filter(question=question)

        results = []
        for test in test_cases:
            payload = {
                "source_code": code,
                "language_id": language_id,
                "stdin": test.input_data
            }
            response = requests.post(JUDGE0_API_URL, json=payload, headers=HEADERS)
            result = response.json()
            results.append({
                "input": test.input_data,
                "expected_output": test.expected_output,
                "actual_output": result.get("stdout", "").strip(),
                "passed": test.expected_output.strip() == result.get("stdout", "").strip()
            })

        return JsonResponse({"results": results})

from django.shortcuts import render

def home(request):
    return render(request, 'testsystem/home.html')
