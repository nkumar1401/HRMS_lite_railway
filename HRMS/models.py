from django.db import models
from django.core.validators import EmailValidator


class Employee(models.Model):
    """Employee model for storing employee information."""
    
    employee_id = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Employee ID",
        help_text="Unique identifier for the employee"
    )
    full_name = models.CharField(
        max_length=100, 
        verbose_name="Full Name"
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Email Address"
    )
    department = models.CharField(
        max_length=100, 
        blank=True, 
        default="",
        verbose_name="Department"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['full_name']
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
    
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


class Attendance(models.Model):
    """Attendance model for tracking employee attendance."""
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name="Employee"
    )
    date = models.DateField(verbose_name="Date")
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES,
        default='present',
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', 'employee__full_name']
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"
        unique_together = ['employee', 'date']  # One attendance record per employee per day
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.get_status_display()})"
