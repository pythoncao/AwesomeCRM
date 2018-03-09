from django.shortcuts import render,redirect
import json




class BaseCocoAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_actions)
    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 20
    actions=[]
    default_actions = ['delete_selected_objs']
    def delete_selected_objs(self,request,querysets):
        querysets_ids = json.dumps([i.id for i in querysets])
        return render(request,'cocoadmin/table_obj_delete.html',{'admin_class':self,
                                                                'objs':querysets ,
                                                                 'querysets_ids':querysets_ids
                                                                 })