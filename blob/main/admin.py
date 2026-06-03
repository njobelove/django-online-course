from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment

# Choice Inline
class ChoiceInline(admin.TabularInline):
    """Inline admin for Choice model"""
    model = Choice
    extra = 4

# Question Inline
class QuestionInline(admin.StackedInline):
    """Stacked inline admin for Question model"""
    model = Question
    extra = 1

# Question Admin
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model"""
    list_display = ['text', 'created_at', 'get_correct_answers']
    list_filter = ['created_at']
    search_fields = ['text']
    inlines = [ChoiceInline]
    
    def get_correct_answers(self, obj):
        return obj.choice_set.filter(is_correct=True).count()
    get_correct_answers.short_description = 'Correct Answers'

# Lesson Admin - ADD THIS (MISSING)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model"""
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model"""
    list_display = ['name', 'instructor', 'duration']
    list_filter = ['instructor']
    search_fields = ['name']

# Register all models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)  # This was missing
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)