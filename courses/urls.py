from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/enroll/', views.enroll_course, name='enroll'),
    path('course/<int:pk>/unenroll/', views.unenroll_course, name='unenroll'),
]