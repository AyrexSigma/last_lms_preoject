from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('course/<int:course_pk>/', views.course_lessons, name='course_lessons'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('assignment/<int:assignment_pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_pk>/grade/', views.grade_submission, name='grade_submission'),

    path('my-courses/', views.my_courses, name='my_courses'),
    path('certificate/<int:course_pk>/download/', views.download_certificate, name='download_certificate'),
]