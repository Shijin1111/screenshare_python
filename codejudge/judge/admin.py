from django.contrib import admin

from .models import Submission,TestCase,Question

admin.site.register(Submission)
admin.site.register(TestCase)
admin.site.register(Question)