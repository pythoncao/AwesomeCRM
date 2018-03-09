from django.contrib import admin
from CRM import models
# Register your models here.


class CostomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['status', ]
    filter_horizontal = ['consult_courses', ]

admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.CustomerInfo,CostomerAdmin)
admin.site.register(models.Student)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Branch)
admin.site.register(models.Menus)
admin.site.register(models.Course)
admin.site.register(models.ContractTemplate)
admin.site.register(models.StudentEnrollment)
admin.site.register(models.PaymentRecord)


