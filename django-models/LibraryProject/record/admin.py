from django.contrib import admin
from .models import StudentAssessmentRecord

# Register your models here.
@admin.register(StudentAssessmentRecord)
class StudentAssessmentRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'score']
