from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Course

def home(request):
    recent_courses = Course.objects.order_by('-created_at')[:6]
    context = {
        'recent_courses': recent_courses,
    }
    return render(request, 'courses/home.html', context)

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        return Course.objects.order_by('-created_at')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user in course.students.all():
        messages.info(request, f'Ви вже записані на курс "{course.title}"')
    else:
        course.students.add(request.user)
        messages.success(request, f'Ви успішно записались на курс "{course.title}"!')
    return redirect('courses:course_detail', pk=pk)

@login_required
def unenroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user in course.students.all():
        course.students.remove(request.user)
        messages.success(request, f'Ви відписались від курсу "{course.title}"')
    return redirect('courses:course_detail', pk=pk)