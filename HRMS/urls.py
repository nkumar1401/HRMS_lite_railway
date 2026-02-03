from django.urls import path
from .views import (
    DashboardView,
    EmployeeListView,
    EmployeeCreateView,
    EmployeeDeleteView,
    AttendanceListView,
    AttendanceCreateView,
    EmployeeAttendanceView,
)

app_name = 'hrms'

urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Employee URLs
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/<int:pk>/attendance/', EmployeeAttendanceView.as_view(), name='employee_attendance'),
    
    # Attendance URLs
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', AttendanceCreateView.as_view(), name='attendance_add'),
]