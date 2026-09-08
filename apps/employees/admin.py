from django.contrib import admin
from .models import Designation, Skill, Certification, Employee, EmployeeSkill, EmployeeCertification

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

class EmployeeCertificationInline(admin.TabularInline):
    model = EmployeeCertification
    extra = 1

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [EmployeeSkillInline, EmployeeCertificationInline]
    list_display = ('employee_id', 'user', 'organization', 'department', 'designation', 'status', 'date_of_joining')
    list_filter = ('organization', 'department', 'status', 'employment_type')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__username', 'user__email')

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'level', 'pay_grade')
    search_fields = ('title', 'code')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'issuing_body', 'validity_years')
    search_fields = ('name', 'code', 'issuing_body')
