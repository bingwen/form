# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Form,Question,Ans,Submit,Subitem

class FormAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Form,FormAdmin)
admin.site.register(Question)
admin.site.register(Ans)
admin.site.register(Submit)
admin.site.register(Subitem)
