# hacks_git

API used:
1. Github API v3 : api.github.com/repos/<owner>/<repo>+/issues
	1.1 Data obtained per request is 100 issues.
	1.2 First, A request to the api end-point with url parameters per_page=100 and access_token(access_token is required to increase api rate limit to 5000 from 60)
	1.3 Next page is obtained using pagining url which is supplied in request response headers.
	1.4 Keep hitting the next paging url till we get "next=first" in paging url.

Future improvement options:
1. Download all the issues in csv with columns as Issue No,Title,body,Created Date,updated date.
2.Charts to show the required data.