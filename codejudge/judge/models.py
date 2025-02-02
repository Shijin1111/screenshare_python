from django.db import models

class Submission(models.Model):
    LANGUAGE_CHOICES = [('python', 'Python'), ('cpp', 'C++'), ('java', 'Java')]
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    input_data = models.TextField()
    output_result = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
