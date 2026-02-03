from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, ListView, CreateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import date, timedelta
from .models import Employee, Attendance
from .forms import EmployeeForm, AttendanceForm, AttendanceFilterForm


class DashboardView(TemplateView):
    """Dashboard view with summary statistics."""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        
        # Employee statistics
        context['total_employees'] = Employee.objects.count()
        
        # Today's attendance
        today_attendance = Attendance.objects.filter(date=today)
        context['today_present'] = today_attendance.filter(status='present').count()
        context['today_absent'] = today_attendance.filter(status='absent').count()
        context['today_total'] = today_attendance.count()
        
        # Calculate attendance rate for today
        if context['total_employees'] > 0:
            context['attendance_rate'] = round(
                (context['today_present'] / context['total_employees']) * 100, 1
            )
        else:
            context['attendance_rate'] = 0
        
        # This week's attendance summary
        week_start = today - timedelta(days=today.weekday())
        week_attendance = Attendance.objects.filter(
            date__gte=week_start, date__lte=today
        )
        context['week_present'] = week_attendance.filter(status='present').count()
        context['week_absent'] = week_attendance.filter(status='absent').count()
        
        # Recent employees (last 5 added)
        context['recent_employees'] = Employee.objects.order_by('-created_at')[:5]
        
        # Recent attendance records (last 10)
        context['recent_attendance'] = Attendance.objects.select_related('employee').order_by('-date', '-created_at')[:10]
        
        return context


class EmployeeListView(ListView):
    """List all employees."""
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(employee_id__icontains=search) |
                Q(full_name__icontains=search) |
                Q(email__icontains=search) |
                Q(department__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['total_count'] = Employee.objects.count()
        return context


class EmployeeCreateView(CreateView):
    """Create a new employee."""
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('hrms:employee_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Employee'
        context['submit_text'] = 'Add Employee'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Employee {self.object.full_name} added successfully!',
                'redirect_url': str(self.success_url)
            })
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)


class EmployeeDeleteView(DeleteView):
    """Delete an employee."""
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('hrms:employee_list')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Employee, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        employee_name = self.object.full_name
        self.object.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Employee {employee_name} deleted successfully!'
            })
        return redirect(self.success_url)
    
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AttendanceListView(ListView):
    """List all attendance records with filtering."""
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendance_records'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('employee')
        
        # Apply filters
        employee_id = self.request.GET.get('employee', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        status = self.request.GET.get('status', '')
        
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AttendanceFilterForm(self.request.GET)
        context['total_count'] = self.get_queryset().count()
        
        # Summary stats
        queryset = self.get_queryset()
        context['present_count'] = queryset.filter(status='present').count()
        context['absent_count'] = queryset.filter(status='absent').count()
        
        return context


class AttendanceCreateView(CreateView):
    """Mark attendance for an employee."""
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('hrms:attendance_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mark Attendance'
        context['submit_text'] = 'Save Attendance'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['date'] = date.today()
        initial['status'] = 'present'
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Attendance marked for {self.object.employee.full_name}!',
                'redirect_url': str(self.success_url)
            })
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)


class EmployeeAttendanceView(DetailView):
    """View attendance records for a specific employee."""
    model = Employee
    template_name = 'attendance/employee_attendance.html'
    context_object_name = 'employee'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get attendance records for this employee
        attendance_records = Attendance.objects.filter(
            employee=self.object
        ).order_by('-date')
        
        # Apply date filters if provided
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        
        if date_from:
            attendance_records = attendance_records.filter(date__gte=date_from)
        if date_to:
            attendance_records = attendance_records.filter(date__lte=date_to)
        
        context['attendance_records'] = attendance_records
        context['total_records'] = attendance_records.count()
        context['present_days'] = attendance_records.filter(status='present').count()
        context['absent_days'] = attendance_records.filter(status='absent').count()
        
        # Calculate attendance percentage
        if context['total_records'] > 0:
            context['attendance_percentage'] = round(
                (context['present_days'] / context['total_records']) * 100, 1
            )
        else:
            context['attendance_percentage'] = 0
        
        context['date_from'] = date_from
        context['date_to'] = date_to
        
        return context


# Error handlers
def custom_404(request, exception):
    """Custom 404 error handler."""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler."""
    return render(request, 'errors/500.html', status=500)