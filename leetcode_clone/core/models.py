# core/models.py
from django.db import models
from django.contrib.auth.models import User
# core/models.py

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_example = models.TextField()
    output_example = models.TextField()
    constraints = models.TextField(null=True)

    # Function signatures for each language (Python, C++, Java)
    expected_python_signature = models.TextField()
    expected_cpp_signature = models.TextField()
    expected_java_signature = models.TextField()

    def __str__(self):
        return self.title

# core/models.py
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name='submissions', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    result = models.CharField(choices=[('pending', 'Pending'), ('passed', 'Passed'), ('failed', 'Failed')], default='pending', max_length=10)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s submission for {self.problem.title}"


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solved_problems = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)

    def __str__(self):
        return f"Leaderboard entry for {self.user.username}"
