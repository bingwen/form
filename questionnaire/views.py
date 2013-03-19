# -*- coding: utf-8 -*-

import os
import time

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.utils import simplejson as json
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.core.servers.basehttp import FileWrapper
from django.contrib.contenttypes.models import ContentType

from django.template import RequestContext
from django.db import transaction
from django.core.context_processors import csrf
from django.utils import timezone

from models import Form,Question,Ans,Submit,Subitem
from django.contrib.auth.models import User

from account.views import requirelogin

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

@requirelogin
def home(request):
	forms = Form.objects.all()
	context = {
		'forms':forms,
	}
	return render_to_response('index.html',context, context_instance=RequestContext(request))

@requirelogin
def statistic(request,form_id):
	try:
		form = Form.objects.get(id=form_id)
	except Exception, e:
		context = {'msg':u"该问卷不存在",}
		return render_to_response('result.html', context,context_instance=RequestContext(request))

	questions = form.question_set.all()


	context = {
		'form':form,
		'form_id':form_id,
		'title':form.title,
		'questions':questions,
	}
	return render_to_response('statistic.html',context, context_instance=RequestContext(request))

@requirelogin
def form(request,form_id):
	try:
		form = Form.objects.get(id=form_id)
	except Exception, e:
		context = {'msg':u"该问卷不存在",}
		return render_to_response('result.html', context,context_instance=RequestContext(request))

	questions = form.question_set.all()

	for x in questions:
		print ">>>",x.ans.all()

	context = {
		'form_id':form_id,
		'title':form.title,
		'questions':questions,
	}
	return render_to_response('form.html',context, context_instance=RequestContext(request))

@requirelogin
def form_submit(request,form_id):

	try:
		form = Form.objects.get(id=form_id)
	except Exception, e:
		context = {'msg':u"该问卷不存在",}
		return render_to_response('result.html', context,context_instance=RequestContext(request))
	try:
		Submit.objects.get(form=form,user=request.user)
		context = {'msg':u"您已经提交过该问卷，请不要重复提交",}
		return render_to_response('result.html', context,context_instance=RequestContext(request))
	except Exception, e:
		pass

	submit = Submit(form=form,user=request.user)
	submit.save()

	
	for key in request.POST:
		try:
			question = Question.objects.get(id=key)
			ans = Ans.objects.get(id=request.POST[key])
			if question and ans:
				subitem = Subitem(submit=submit,question=question,ans=ans)
				subitem.save()
				print ">>>>subitem:%s,%s" % (question,ans)
		except Exception, e:
			pass
	context = {'msg':"Success",}	
	return render_to_response('result.html', context,context_instance=RequestContext(request))

@requirelogin
def submit(request,form_id,user_id):
	try:
		form = Form.objects.get(id=form_id)
	except Exception, e:
		context = {'msg':u"该问卷不存在",}
		return render_to_response('result.html', context,context_instance=RequestContext(request))
	try:
		user = User.objects.get(id=user_id)
		submit = Submit.objects.get(form=form,user=user)
	except Exception, e:
		context = {'msg':(user.username+u"还未提交过问卷"+form.title),}
		return render_to_response('result.html', context,context_instance=RequestContext(request))
	
	questions = form.question_set.all()

	ans_str = u""
	index = 1
	for question in questions:
		ans_str += """<div class="question"><div class="qu_title">%s.%s</div><div class="qu_ans_list">""" % (index,question.title)
		for an in question.ans.all():
			selected = False
			try:
				subitem = Subitem.objects.get(ans=an,submit=submit)
				selected = True
			except Exception, e:
				pass
			if selected:
				ans_str+="""<div class="qu_ans"><i class="icon-ok"></i><label>%s</label></div>""" % an.title
			else:
				ans_str+="""<div class="qu_ans">&nbsp;&nbsp;&nbsp;&nbsp;<label>%s</label></div>""" % an.title
        ans_str += """</div></div>"""
		index += 1
	print ">>>>",ans_str
	context = {
		'ans_str':ans_str,
		'form':form,
		'form_id':form_id,
		'submit':submit,
		'title':form.title+'-'+user.username,
		'questions':questions,
	}
	return render_to_response('submit_user.html',context, context_instance=RequestContext(request))
