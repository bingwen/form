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

import string
nums = string.digits
def check(a):
	if type(a) is not str:
		return False
	else:
		for i in a:
			if i not in nums:
				return False
		return True

def home(request):
	forms = Form.objects.all()

	context = {
		'forms':forms,
	}
	return render_to_response('index.html',context, context_instance=RequestContext(request))

def statistic(request,form_id):
	print ">>>>form_id:",form_id
	form = Form.objects.get(id=form_id)
	print ">>>>",form.title
	questions = form.question_set.all()
	print ">>>>",questions

	for x in questions:
		print ">>>",x.ans.all()

	context = {
		'form_id':form_id,
		'title':form.title,
		'questions':questions,
	}
	return render_to_response('statistic.html',context, context_instance=RequestContext(request))

def form(request,form_id):
	print ">>>>form_id:",form_id
	form = Form.objects.get(id=form_id)
	print ">>>>",form.title
	questions = form.question_set.all()
	print ">>>>",questions

	for x in questions:
		print ">>>",x.ans.all()

	context = {
		'form_id':form_id,
		'title':form.title,
		'questions':questions,
	}
	return render_to_response('form.html',context, context_instance=RequestContext(request))

def form_submit(request,form_id):
	print ">>>>form_id:",form_id
	form = Form.objects.get(id=form_id)
	if not form:
		pass
	submit = Submit(form=form)
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
		

		
	return render_to_response('result.html', context_instance=RequestContext(request))