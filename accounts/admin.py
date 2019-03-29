from django.contrib import admin
from .models import User
from tests.models import TestResult


class TestResultsInline(admin.TabularInline):
    model = TestResult


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [TestResultsInline]
