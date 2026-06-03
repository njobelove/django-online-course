from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    """Model for storing exam questions"""
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text[:50]
    
    def get_correct_choices(self):
        """Return all correct choices for this question"""
        return self.choice_set.filter(is_correct=True)

class Choice(models.Model):
    """Model for storing answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Enrollment(models.Model):
    """Model for tracking student enrollment in courses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"

class Submission(models.Model):
    """Model for storing student exam submissions"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['enrollment', 'question']
    
    def __str__(self):
        return f"{self.enrollment.user.username} - {self.question.text[:30]} - {'Correct' if self.is_correct else 'Incorrect'}"
    
    def is_get_score(self):
        """Return score for this submission (1 if correct, 0 if incorrect)"""
        return 1 if self.is_correct else 0