"""
Employee Management Services
"""
from apps.employees.models import Employee


class EmployeeService:
    @staticmethod
    def get_employee_workload(employee_id):
        emp = Employee.objects.prefetch_related('assigned_work_orders').get(id=employee_id)
        wos = emp.assigned_work_orders.all()
        return {
            'employee_name': emp.user.get_full_name(),
            'designation': emp.designation.title if emp.designation else None,
            'active_work_orders_count': wos.filter(status__in=['ASSIGNED', 'IN_PROGRESS']).count(),
            'completed_work_orders_count': wos.filter(status='COMPLETED').count(),
        }
