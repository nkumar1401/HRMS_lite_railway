from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .models import Employee, Attendance
import re


class EmployeeForm(forms.ModelForm):
    """Form for creating and updating Employee records."""
    
    class Meta:
        model = Employee
        fields = ['employee_id', 'full_name', 'email', 'department']
        widgets = {
            'employee_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter unique employee ID (e.g., EMP001)',
                'id': 'employee_id',
                'autocomplete': 'off',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter full name',
                'id': 'full_name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter email address',
                'id': 'email',
                'autocomplete': 'email',
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter department (optional)',
                'id': 'department',
                'autocomplete': 'off',
            }),
        }
    
    def clean_employee_id(self):
        """Validate employee ID format and uniqueness."""
        employee_id = self.cleaned_data.get('employee_id', '').strip()
        if not employee_id:
            raise ValidationError("Employee ID is required.")
        
        # Check uniqueness (excluding current instance for updates)
        queryset = Employee.objects.filter(employee_id__iexact=employee_id)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("An employee with this ID already exists.")
        
        return employee_id.upper()
    
    def clean_full_name(self):
        """Validate full name."""
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not full_name:
            raise ValidationError("Full name is required.")
        if len(full_name) < 2:
            raise ValidationError("Full name must be at least 2 characters.")
        return full_name
    
    def clean_email(self):
        """Validate email format and uniqueness."""
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("Email address is required.")
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Please enter a valid email address.")
        
        # Check uniqueness (excluding current instance for updates)
        queryset = Employee.objects.filter(email__iexact=email)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("An employee with this email already exists.")
        
        return email


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance."""
    
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status']
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'form-select',
                'id': 'employee',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'id': 'attendance_date',
            }),
            'status': forms.RadioSelect(attrs={
                'class': 'form-radio',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set employee queryset with nice display
        self.fields['employee'].queryset = Employee.objects.all().order_by('full_name')
        self.fields['employee'].empty_label = "-- Select an Employee --"
    
    def clean(self):
        """Validate attendance record uniqueness."""
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        date = cleaned_data.get('date')
        
        if employee and date:
            # Check if attendance already exists for this employee on this date
            queryset = Attendance.objects.filter(employee=employee, date=date)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise ValidationError(
                    f"Attendance for {employee.full_name} on {date} already exists."
                )
        
        return cleaned_data


class AttendanceFilterForm(forms.Form):
    """Form for filtering attendance records."""
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all().order_by('full_name'),
        required=False,
        empty_label="All Employees",
        widget=forms.Select(attrs={
            'class': 'form-select filter-select',
            'id': 'filter_employee',
        })
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input filter-input',
            'type': 'date',
            'id': 'filter_date_from',
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input filter-input',
            'type': 'date',
            'id': 'filter_date_to',
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses'), ('present', 'Present'), ('absent', 'Absent')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select filter-select',
            'id': 'filter_status',
        })
    )
