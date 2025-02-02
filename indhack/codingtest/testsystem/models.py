from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input_data = models.TextField()
    expected_output = models.TextField()
