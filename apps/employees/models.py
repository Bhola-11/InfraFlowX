import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization, Department, Office, Team

class Designation(models.Model):
    """
    Formal job titles and pay grades within the infrastructure agency.
    """
    title = models.CharField(max_length=150, unique=True, verbose_name=_('Job Designation Title'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Designation Code'))
    level = models.IntegerField(default=1, verbose_name=_('Hierarchy Level (1-10)'))
    pay_grade = models.CharField(max_length=50, blank=True, verbose_name=_('Pay Grade'))
    description = models.TextField(blank=True, verbose_name=_('Job Description & Requirements'))

    class Meta:
        ordering = ['level', 'title']
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')

    def __str__(self):
        return f"{self.title} (L{self.level})"


class Skill(models.Model):
    """
    Technical and operational competencies (e.g. Ultrasonic NDT, Asphalt Compaction, GIS Analysis).
    """
    CATEGORY_CHOICES = [
        ('CIVIL', _('Civil & Structural Engineering')),
        ('ELECTRICAL', _('Electrical & Power Systems')),
        ('MECHANICAL', _('Mechanical & Heavy Plant')),
        ('GIS_SURVEY', _('GIS & Topographic Survey')),
        ('SAFETY', _('Occupational Health & Safety')),
        ('PROJECT_MGMT', _('Project & Contract Management')),
        ('INSPECTION', _('Quality & Non-Destructive Inspection')),
    ]

    name = models.CharField(max_length=150, unique=True, verbose_name=_('Skill Name'))
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='CIVIL', verbose_name=_('Skill Category'))
    description = models.TextField(blank=True, verbose_name=_('Skill Description'))

    class Meta:
        ordering = ['category', 'name']
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')

    def __str__(self):
        return f"{self.name} [{self.get_category_display()}]"


class Certification(models.Model):
    """
    Professional industry certifications, state licenses, and safety permits.
    """
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Certification / License Name'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Certification Code'))
    issuing_body = models.CharField(max_length=200, verbose_name=_('Issuing Regulatory Body'))
    validity_years = models.IntegerField(default=3, verbose_name=_('Validity Period (Years)'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Certification')
        verbose_name_plural = _('Certifications')

    def __str__(self):
        return f"{self.name} ({self.issuing_body})"


class Employee(models.Model):
    """
    Core employee record linking to user credentials, organizational units, and supervisor chains.
    """
    EMPLOYMENT_TYPES = [
        ('FULL_TIME', _('Full Time Permanent')),
        ('CONTRACT', _('Contractual / Project-Based')),
        ('CIVIL_SERVANT', _('Government / Civil Servant')),
        ('CONSULTANT', _('Technical Consultant')),
        ('INTERN', _('Apprentice / Trainee')),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', _('Active / On Duty')),
        ('ON_LEAVE', _('On Approved Leave')),
        ('FIELD_ASSIGNMENT', _('On Remote Field Assignment')),
        ('SUSPENDED', _('Suspended')),
        ('TERMINATED', _('Terminated / Relieved')),
        ('RETIRED', _('Retired')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name=_('User Account')
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Official Employee ID')
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name=_('Organization')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name=_('Department')
    )
    office = models.ForeignKey(
        Office,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name=_('Base Office')
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name=_('Assigned Team')
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='holders',
        verbose_name=_('Job Designation')
    )
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name=_('Direct Supervisor / Manager')
    )
    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPES,
        default='FULL_TIME',
        verbose_name=_('Employment Type')
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        db_index=True,
        verbose_name=_('Employment Status')
    )
    date_of_joining = models.DateField(
        verbose_name=_('Date of Joining')
    )
    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Emergency Contact Person')
    )
    emergency_contact_phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Emergency Contact Phone')
    )
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Annual Compensation ($)')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id}) - {self.designation.title if self.designation else 'Staff'}"


class EmployeeSkill(models.Model):
    """
    Skill rating and experience tracking for employees.
    """
    PROFICIENCY_LEVELS = [
        (1, _('1 - Novice / Basic Knowledge')),
        (2, _('2 - Intermediate / Supervised Work')),
        (3, _('3 - Competent / Independent Practitioner')),
        (4, _('4 - Advanced / Lead Specialist')),
        (5, _('5 - Expert / Master Authority')),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name=_('Employee')
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='certified_employees',
        verbose_name=_('Skill')
    )
    proficiency = models.IntegerField(
        choices=PROFICIENCY_LEVELS,
        default=3,
        verbose_name=_('Proficiency Level')
    )
    years_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=1.0,
        verbose_name=_('Years of Practical Experience')
    )

    class Meta:
        unique_together = ('employee', 'skill')
        verbose_name = _('Employee Skill')
        verbose_name_plural = _('Employee Skills')

    def __str__(self):
        return f"{self.employee.user.username} - {self.skill.name} (Level {self.proficiency})"


class EmployeeCertification(models.Model):
    """
    Verified regulatory and professional certifications held by employees.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='certifications',
        verbose_name=_('Employee')
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        related_name='holders',
        verbose_name=_('Certification')
    )
    certificate_number = models.CharField(
        max_length=100,
        verbose_name=_('Certificate / License Number')
    )
    issue_date = models.DateField(
        verbose_name=_('Issue Date')
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Expiry Date')
    )
    certificate_file = models.FileField(
        upload_to='certifications/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_('Certificate Document Copy')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Verified by Compliance / HR')
    )

    class Meta:
        verbose_name = _('Employee Certification')
        verbose_name_plural = _('Employee Certifications')

    def __str__(self):
        return f"{self.employee.user.username} - {self.certification.name} ({self.certificate_number})"
