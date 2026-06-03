from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment

# Choice Inline - for adding choices directly in Question admin
class ChoiceInline(admin.TabularInline):
    """Inline admin for Choice model"""
    model = Choice
    extra = 4

# Question Inline - for adding questions in Course admin
class QuestionInline(admin.StackedInline):
    """Stacked inline admin for Question model"""
    model = Question
    extra = 1
    show_change_link = True

# Question Admin
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model"""
    list_display = ['text', 'grade', 'course', 'created_at', 'get_correct_answers']
    list_filter = ['course', 'created_at']
    search_fields = ['text']
    inlines = [ChoiceInline]
    
    def get_correct_answers(self, obj):
        return obj.choice_set.filter(is_correct=True).count()
    get_correct_answers.short_description = 'Correct Answers'

# Lesson Admin
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model"""
    list_display = ['title', 'course', 'order', 'duration']
    list_filter = ['course']
    search_fields = ['title']

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model"""
    list_display = ['name', 'instructor', 'duration', 'lesson_count']
    list_filter = ['instructor']
    search_fields = ['name']
    inlines = [QuestionInline]
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Number of Lessons'

# Instructor Admin
class InstructorAdmin(admin.ModelAdmin):
    """Admin configuration for Instructor model"""
    list_display = ['user', 'expertise']
    search_fields = ['user__username']

# Learner Admin
class LearnerAdmin(admin.ModelAdmin):
    """Admin configuration for Learner model"""
    list_display = ['user', 'enrolled_courses_count']
    search_fields = ['user__username']
    
    def enrolled_courses_count(self, obj):
        return obj.enrolled_courses.count()
    enrolled_courses_count.short_description = 'Enrolled Courses'

# Enrollment Admin
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model"""
    list_display = ['user', 'course', 'enrolled_at']
    list_filter = ['course', 'enrolled_at']
    search_fields = ['user__username', 'course__name']

# Submission Admin
class SubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for Submission model"""
    list_display = ['enrollment', 'question', 'submitted_at', 'score']
    list_filter = ['submitted_at']
    
    def score(self, obj):
        return obj.is_get_score()
    score.short_description = 'Score'

# Register all models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
