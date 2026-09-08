from django.contrib import admin
from .models import Organization, Region, Zone, Department, Office, Team

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'org_type', 'is_active', 'annual_budget', 'created_at')
    list_filter = ('org_type', 'is_active')
    search_fields = ('name', 'code', 'tax_id')

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'regional_head')
    list_filter = ('organization',)
    search_fields = ('name', 'code')

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'region')
    list_filter = ('region__organization', 'region')
    search_fields = ('name', 'code')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'head_of_department', 'budget_allocation')
    list_filter = ('organization',)
    search_fields = ('name', 'code')

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'region', 'office_type', 'phone')
    list_filter = ('organization', 'office_type')
    search_fields = ('name', 'address')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'office', 'team_lead')
    list_filter = ('department__organization', 'department')
    search_fields = ('name', 'code', 'specialization')
