from django import conf



def cocoadmin_auto_discover():

    for app_name in conf.settings.INSTALLED_APPS:
        # print('adfdffffdfsfafafdfafa-------------------------------')
        # mod = __import__('%s.cocoadmin' % app_name)
        # print(mod.cocoadmin)

        try:
            mod = __import__('%s.cocoadmin' % app_name)
            print(mod.cocoadmin)
        except ImportError:
            pass
