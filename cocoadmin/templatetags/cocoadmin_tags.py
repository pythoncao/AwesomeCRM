from django.template import Library
from django.utils.safestring import mark_safe
import datetime


register = Library()

@register.simple_tag
def build_filter_ele(filter_coloum,admin_class):

    coloum_obj = admin_class.model._meta.get_field(filter_coloum)
    # print(filter_coloum, admin_class.filter_conditiond)
    try:
        filter_ele = "<select name='%s'>" % filter_coloum
        for choice in coloum_obj.get_choices():
            selected = ''

            if filter_coloum in admin_class.filter_conditions:

                if str(choice[0]) == admin_class.filter_conditions.get(filter_coloum):
                    selected = 'selected'
            option = "<option value='%s'%s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option

            # print(choice[0],choice[1])
    except AttributeError as e:
        # print("err", e)
        filter_ele = "<select name='%s__gte'>" % filter_coloum
        if coloum_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['', '------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
                ['', 'ALL'],
            ]

            for i in time_list:
                selected = ''
                time_to_str = ''if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if "%s__gte"%filter_coloum in admin_class.filter_conditions:

                    if time_to_str == admin_class.filter_conditions.get("%s__gte"%filter_coloum):
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" %\
                         (time_to_str, selected , i[1])
                # print(i[0].year)
                filter_ele += option

    filter_ele += "</select>"
    return mark_safe(filter_ele)




@register.simple_tag
def build_table_row(obj,admin_class):
    """生成一条html"""

    ele = ''
    if admin_class.list_display:
        for index, coloum_name in enumerate(admin_class.list_display):
            coloum_obj = admin_class.model._meta.get_field(coloum_name)
            if coloum_obj.choices:
                coloum_data = getattr(obj,'get_%s_display'%coloum_name)()
            else:
                coloum_data = getattr(obj,coloum_name)

            td_ele = "<td>%s</td>" % coloum_data
            if index == 0:
                td_ele = '<td><a href="%s/change/">%s</a></td>' % (obj.id, coloum_data)
            ele += td_ele
    else:
        td_ele = '<td><a href="%s/change/">%s</a></td>' % (obj.id, obj)
        ele += td_ele
    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()

@register.simple_tag
def render_filter_args(admin_class,render_html = True):
    if admin_class.filter_conditions:
        ele = ''
        for k,v in admin_class.filter_conditions.items():
            ele += '&%s=%s'%(k,v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''






@register.simple_tag
def get_sorted_coloum(row,sorted_coloum, forloop):

    if row in sorted_coloum:
        last_sort_index = sorted_coloum[row]
        if last_sort_index.startswith("-"):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-%s'%last_sort_index
        return this_time_sort_index
    else:
        return forloop


@register.simple_tag
def render_paginator(querysets, admin_class, sorted_coloum):
    ele = """
      <ul class="pagination">       
    """
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i)<2:
            active = ''
            if querysets.number == i:
                active = 'active'
            filter_ele = render_filter_args(admin_class)
            sorted_ele = ''
            if sorted_coloum:
                sorted_ele = "&_o=%s" %list(sorted_coloum.values())[0]

            p_ele ="""<li class="%s"><a href="?page=%s%s%s">%s</a></li>"""%(active,i,filter_ele,sorted_ele,i)
            ele += p_ele

    ele += "</ul>"

    return mark_safe(ele)

@register.simple_tag
def get_current_coloum_index(sorted_coloum):
    return list(sorted_coloum.values())[0] if sorted_coloum else ''

@register.simple_tag
def get_obj_field_val(form_obj, field):
    """返回model obj具体字段的值"""

    return getattr(form_obj.instance, field)

@register.simple_tag
def get_available_m2m_data(field_name, form_obj, admin_class):
    """返回的是m2m字段关联表的所有数据"""
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance, field_name).all())
        return obj_list-selected_data
    else:
        return obj_list

@register.simple_tag
def get_selected_m2m_data(field_name, form_obj, admin_class):
    """返回的是m2m字段已选的数据"""
    if form_obj.instance.id:
        selected_data = getattr(form_obj.instance, field_name).all()
        return selected_data
    else:
        return []

@register.simple_tag
def get_model_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name



@register.simple_tag
def display_all_related_objs(obj):
    """显示要被删除对想的关联对象（所有）"""


    ele = "<ul>"
    # ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" %(obj._meta.app_label,
    #                                                                  obj._meta.model_name,
    #                                                                  obj.id,obj)

    for reversed_fk_obj in obj._meta.related_objects:

        related_table_name =  reversed_fk_obj.name
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj,related_lookup_key).all() #反向查所有关联的数据
        ele += "<li>%s3333<ul> "% related_table_name

        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/cocoadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label,i._meta.model_name,i.id,i,obj)
        else:
            for i in related_objs:
                #ele += "<li>%s--</li>" %i
                ele += "<li><a href='/cocoadmin/%s/%s/%s/change/'>%s</a></li>" %(i._meta.app_label,
                                                                                 i._meta.model_name,
                                                                                 i.id,i)
                ele += display_all_related_objs(i)

        ele += "</ul></li>"

    ele += "</ul>"

    return ele