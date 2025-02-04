# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=6)
    input_example = models.TextField()
    output_example = models.TextField()
    constraints = models.TextField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name='submissions', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    result = models.CharField(choices=[('pending', 'Pending'), ('passed', 'Passed'), ('failed', 'Failed')], default='pending', max_length=10)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.problem.title}"

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solved_problems = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)

    def __str__(self):
        return f"Leaderboard entry for {self.user.username}"
