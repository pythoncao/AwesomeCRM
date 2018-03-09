
from CRM import models
from cocoadmin.sites import site
from cocoadmin.admin_base import BaseCocoAdmin

class CostomerAdmin(BaseCocoAdmin):
    list_display = ['name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['status','contact']
    filter_horizontal = ['consult_courses', ]
    actions = ['change_status',]
    def change_status(self,request,querysets):
        querysets.update(status=0)

site.register(models.CustomerInfo,CostomerAdmin)
site.register(models.Role)
site.register(models.Menus)
site.register(models.UserProfile)
site.register(models.Course)
site.register(models.ClassList)
site.register(models.CourseRecord)
site.register(models.StudyRecord)
