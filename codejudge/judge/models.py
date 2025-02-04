from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")])

    def __str__(self):
        return self.title

from django.contrib.postgres.fields import ArrayField  
class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="test_cases")
    input_data = models.JSONField()  # This will store dynamic input data (list, dict, etc.)
    expected_output = models.JSONField()  # Store the expected output as a string


class Submission(models.Model):
    user = models.CharField(max_length=100)  # Can be linked to auth user
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10, choices=[("python", "Python"), ("cpp", "C++"), ("java", "Java")])
    status = models.CharField(max_length=20, default="Pending")  # "Pending", "Accepted", "Wrong Answer", "Error"
    timestamp = models.DateTimeField(auto_now_add=True)
