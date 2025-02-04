from django.contrib import admin

from .models import Submission,TestCase,Question

admin.site.register(Submission)
admin.site.register(Question)

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'input_data', 'expected_output')  # Customize the list view
    search_fields = ('question__title',)  # Optionally search by question title
