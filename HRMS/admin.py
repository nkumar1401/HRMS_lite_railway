from django.contrib import admin
from .models import Employee, Attendance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin configuration for Employee model."""
    
    list_display = ('employee_id', 'full_name', 'email', 'department', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('employee_id', 'full_name', 'email', 'department')
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin configuration for Attendance model."""
    
    list_display = ('employee', 'date', 'status', 'created_at')
    list_filter = ('status', 'date', 'employee')
    search_fields = ('employee__full_name', 'employee__employee_id')
    date_hierarchy = 'date'
    ordering = ('-date',)
    readonly_fields = ('created_at',)
