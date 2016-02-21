from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse 
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.conf import settings
import os
from lib import git_lib

def home_page(request):
	template_context = {'settings': settings}
	return render_to_response('home.html', template_context, context_instance=RequestContext(request))

def process_repo(request):
	if request.method=='POST':
		print request.POST['repo_name']
		try:
			repo_name=request.POST['repo_name'].split('/')[-2:]
			print repo_name[0],repo_name[1]
		except IndexError:
			return HttpResponse('Please enter repo path in valid format like <b>https://github.com/Shippable/support</b>')
		git_issues_data=git_lib.get_git_data(owner=repo_name[0],repo=repo_name[1])
		if 'error' in git_issues_data:
			return HttpResponse(git_issues_data['error'])
		else:
			for git_data in git_issues_data:
				git_issues_data[git_data]=len(git_issues_data[git_data])
			git_issues_data['total']=sum(git_issues_data.values())
			git_issues_data['repo']=request.POST['repo_name']
			print git_issues_data
			template_context={'data':git_issues_data}
			return render_to_response('show_git_data.html', template_context, context_instance=RequestContext(request))
	else:
		return HttpResponse('Form data was not sent through post method.')

#def download_csv(request):
#	pass
#	response = HttpResponse(content_type='text/csv')
#	response['Content-Disposition'] = 'attachment; filename="data.csv"'
#	writer = csv.writer(response)
#	writer.writerow(datas[0].keys())
#	for data in datas:
#		writer.writerow(data.values())
#	return response
