import requests
import time
import datetime
from django.conf import settings
	
def convert_to_unixtime(date):
	return int(time.mktime(datetime.datetime.strptime(date.split('+')[0],"%Y-%m-%dT%H:%M:%SZ").timetuple()))

def get_requests(data_return,url):
	now_time=int(time.time())
	r= requests.get(url)
	#printing api requests remaining per hour.
	print r.status_code
	print r.headers['X-RateLimit-Limit']
	print r.headers['X-RateLimit-Remaining']
	
	if r and r.status_code==requests.codes.ok:
		add_data=r.json()
		if add_data:
			for add_data_value in add_data:
				#logic to get classify issues according to given dates
				add_data_value_timestamp=(now_time-convert_to_unixtime(add_data_value['created_at']))
				#print 21,add_data_value_timestamp
				if add_data_value_timestamp <86400:
					data_return['24_hr'].append(add_data_value)
				elif add_data_value_timestamp > 86400 and add_data_value_timestamp < 604800:
					data_return['less_7_day'].append(add_data_value)
				elif add_data_value_timestamp > 604800:
					data_return['more_7_day'].append(add_data_value)
			#Fetching url for pagination and cleaning the obtained string to get only the url
			pageing_url=r.headers['LINK'].split(',')[0]
			if pageing_url.find('first')>=0:
				return False
			else:
				next_url=pageing_url.split(';')[0].strip('< >')
				print r.headers['LINK'].split(',')[0]
				return next_url
		else:
			return False
	elif r.status_code==404:
		return 'No such repo'
	elif r.status_code==403:
		return 'Rate Limit of expired.'


def get_git_data(owner="Shippable",repo="support"):
	data_return={}
	data_return['24_hr']=[]
	data_return['less_7_day']=[]
	data_return['more_7_day']=[]
	print settings.GIT_TOKEN
	#API end-pt
	url= "https://api.github.com/repos/"+str(owner)+'/'+str(repo)+"/issues?per_page=100&access_token="+str(settings.GIT_TOKEN)
	url= get_requests(data_return,url)
	print 47,url
	while url:
		if url is False:
			break
		elif url=='No such repo' or url=='Rate Limit of expired.':
			data_return['error']=url
			break
		url= get_requests(data_return,url)
	#print len(data_return)
	#for i in data_return:
	#	print 'TRACER',i
	#	for j in data_return[i]:
	#		print j['number'],j['title']
	return data_return

if __name__ == '__main__':
	get_git_data()