

from cocoadmin.admin_base import BaseCocoAdmin


class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}



    def register(self,model_class,admin_class=None):
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        print(model_class, admin_class)
        if not admin_class:
            admin_class = BaseCocoAdmin()
        else:
            admin_class = admin_class()



        admin_class.model = model_class #吧model_class赋值给admin_class



        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name]={}
        self.enabled_admins[app_name][model_name] = admin_class


site = AdminSite()