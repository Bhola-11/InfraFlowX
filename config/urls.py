"""
URL Configuration for InfraFlowX project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Root redirect to main dashboard or login
    path('', lambda request: redirect('analytics:dashboard'), name='root'),
    
    # Enterprise Applications Routing
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('organizations/', include('apps.organizations.urls', namespace='organizations')),
    path('employees/', include('apps.employees.urls', namespace='employees')),
    path('assets/', include('apps.assets.urls', namespace='assets')),
    path('roads/', include('apps.roads.urls', namespace='roads')),
    path('bridges/', include('apps.bridges.urls', namespace='bridges')),
    path('buildings/', include('apps.buildings.urls', namespace='buildings')),
    path('facilities/', include('apps.facilities.urls', namespace='facilities')),
    path('locations/', include('apps.locations.urls', namespace='locations')),
    path('inspections/', include('apps.inspections.urls', namespace='inspections')),
    path('conditions/', include('apps.conditions.urls', namespace='conditions')),
    path('maintenance/', include('apps.maintenance.urls', namespace='maintenance')),
    path('workorders/', include('apps.workorders.urls', namespace='workorders')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('contractors/', include('apps.contractors.urls', namespace='contractors')),
    path('budgets/', include('apps.budgets.urls', namespace='budgets')),
    path('expenses/', include('apps.expenses.urls', namespace='expenses')),
    path('incidents/', include('apps.incidents.urls', namespace='incidents')),
    path('documents/', include('apps.documents.urls', namespace='documents')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('schedules/', include('apps.schedules.urls', namespace='schedules')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('support/', include('apps.support.urls', namespace='support')),
    path('permissions/', include('apps.permissions.urls', namespace='permissions')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
