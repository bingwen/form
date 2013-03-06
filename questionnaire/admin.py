# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Form,Question,Ans,Submit,Subitem


admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Ans)
admin.site.register(Submit)
admin.site.register(Subitem)
