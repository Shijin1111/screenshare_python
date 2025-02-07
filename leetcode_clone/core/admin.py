from django.contrib import admin

# Register your models here.
from .models import Submission,Problem,Leaderboard,TestCase
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Leaderboard)


from django.contrib import admin
from .models import TestCase



admin.site.register(TestCase)
