from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Choice, Submission, Enrollment, Course

@login_required
def submit(request, course_id, question_id):
    """Handle question submission and save user's answer"""
    course = get_object_or_404(Course, id=course_id)
    question = get_object_or_404(Question, id=question_id)
    
    # Get or create enrollment
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            
            # Check if user already submitted this question
            submission, created = Submission.objects.get_or_create(
                enrollment=enrollment,
                question=question,
                defaults={'selected_choice': selected_choice}
            )
            
            if not created:
                # Update existing submission
                submission.selected_choice = selected_choice
                submission.submitted_at = timezone.now()
            
            submission.is_correct = selected_choice.is_correct
            submission.save()
            
            messages.success(request, "Your answer has been submitted!")
        else:
            messages.error(request, "Please select an answer.")
    
    # Redirect to exam results
    return redirect('show_exam_result', course_id=course.id)

@login_required
def show_exam_result(request, course_id):
    """Display exam results with score and congratulations message"""
    course = get_object_or_404(Course, id=course_id)
    
    # Get enrollment
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')
    
    # Get all submissions for this enrollment
    submissions = Submission.objects.filter(enrollment=enrollment)
    
    # Calculate scores
    total_questions = Question.objects.count()
    total_score = sum([sub.is_get_score() for sub in submissions])
    possible_score = total_questions
    
    score_percentage = (total_score / possible_score * 100) if possible_score > 0 else 0
    passed = score_percentage >= 70
    
    context = {
        'course': course,
        'submissions': submissions,
        'total_score': total_score,
        'possible_score': possible_score,
        'score_percentage': round(score_percentage, 2),
        'passed': passed,
        'congratulations': passed,
    }
    
    return render(request, 'exam_result.html', context)