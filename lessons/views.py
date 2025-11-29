from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from courses.models import Course
from .models import Lesson, Assignment, Submission
from .forms import SubmissionForm
from .utils import generate_certificate_pdf
@login_required
def course_lessons(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user not in course.students.all() and request.user != course.teacher and not request.user.is_staff:
        messages.error(request, 'У вас немає доступу до цього курсу')
        return redirect('courses:course_list')
    return render(request, 'lessons/course_lessons.html', {'course': course})

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        if self.request.user.is_authenticated:
            context['submission'] = Submission.objects.filter(
                assignment__lesson=self.object,
                student=self.request.user
            ).first()
        return context

@login_required
def submit_assignment(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    course = assignment.lesson.course

    if request.user not in course.students.all():
        messages.error(request, 'Ви не записані на цей курс')
        return redirect('courses:course_list')

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Завдання успішно здано!')
            return redirect('lessons:lesson_detail', pk=assignment.lesson.pk)
    else:
        form = SubmissionForm()
    return render(request, 'lessons/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
        'course': course
    })

@login_required
def grade_submission(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    course = submission.assignment.lesson.course

    if request.user != course.teacher and not request.user.is_staff:
        messages.error(request, 'Ви не можете оцінювати це завдання')
        return redirect('courses:course_list')

    if request.method == 'POST':
        score = request.POST.get('score')
        feedback = request.POST.get('feedback')
        submission.score = score
        submission.feedback = feedback
        submission.save()
        messages.success(request, f'Оцінка {score} успішно виставлена')
        return redirect('lessons:lesson_detail', pk=submission.assignment.lesson.pk)

    return render(request, 'lessons/grade_submission.html', {
        'submission': submission,
        'course': course
    })

@login_required
def my_courses(request):
    enrolled = request.user.enrolled_courses.all()

    courses_with_progress = []
    completed_courses = []

    for course in enrolled:
        total = 0
        done = 0
        for lesson in course.lessons.all():
            total += lesson.assignments.count()
            done += lesson.assignments.filter(
                submissions__student=request.user,
                submissions__score__isnull=False
            ).count()

        progress = int(done / total * 100) if total > 0 else 0
        courses_with_progress.append({
            'course': course,
            'progress': progress,
            'total': total,
            'done': done
        })

        if progress == 100:
            completed_courses.append((course, progress))

    context = {
        'courses_with_progress': courses_with_progress,
        'completed_courses': completed_courses,
    }
    return render(request, 'lessons/my_courses.html', context)

@login_required
def download_certificate(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, students=request.user)
    total = sum(l.assignments.count() for l in course.lessons.all())
    done = sum(l.assignments.filter(submissions__student=request.user, submissions__score__isnull=False).count()
               for l in course.lessons.all())
    if total > 0 and done == total:
        return generate_certificate_pdf(request.user, course)
    else:
        messages.error(request, 'Сертифікат доступний тільки після 100% виконання всіх завдань')
        return redirect('lessons:my_courses')