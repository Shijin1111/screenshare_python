# core/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Problem, Submission, Leaderboard
from django.contrib.auth.decorators import login_required

# View to display all problems
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'core/problem_list.html', {'problems': problems})

# View to display details of a problem
def problem_detail(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    return render(request, 'core/problem_detail.html', {'problem': problem})

# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission
from .utils import evaluate_code

# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission
from .utils import evaluate_code

@login_required
def submit_solution(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    
    if request.method == "POST":
        code = request.POST['code']
        language = request.POST['language']

        # Store the submission
        submission = Submission.objects.create(
            user=request.user,
            problem_id=problem_id,
            code=code,
            language=language,
            result="pending"
        )

        # Evaluate the code based on the selected language
        result = evaluate_code(code, language, problem_id)

        # Update the submission result
        submission.result = result
        submission.save()

        return redirect('core:problem_list')

    return render(request, 'core/submit_solution.html', {
        'problem': problem,
        'python_signature': problem.expected_python_signature,
        'cpp_signature': problem.expected_cpp_signature,
        'java_signature': problem.expected_java_signature,
    })
