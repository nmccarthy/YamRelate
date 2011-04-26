# Created by Neil McCarthy, Implementation Engineer, Yammer, nmccarthy-inc@yammer.com
# v0.1, 04/20/2011

# yammeredge@muchomail.com -> 4876628
# nmccarthy@muchomail.com -> 4360939

import sys, httplib, simplejson, csv, time

# here is the oath token, replace it with your own
oauthToken = 'TODO'
csvFilename = 'TODO.csv'

# time delay to prevent rate limiting
tdelay=0

# initiate connection to Yammer (must be https)
yamconn = httplib.HTTPSConnection("www.yammer.com")

emailList = csv.reader(open(csvFilename, 'rb'), delimiter=',')

for row in emailList:
	selectedEmail = row[0]

	# find user by email address so we can get their id
	findEndPoint='/api/v1/users/by_email.json?access_token=' + oauthToken + '&email=' + selectedEmail
	yamconn.request('GET', findEndPoint)

	# process json from yammer.com -> convert to python dict
	time.sleep(tdelay)
	userraw = yamconn.getresponse()
	userread = userraw.read()
	selectedUser = simplejson.loads(userread)

	# get the id of the user, if they exist
	try:
		selectedUserId = selectedUser[0]['id']
	except IndexError:
		print selectedEmail + ' does not exist.'
		continue
	
	selectedUserIdstr = str(selectedUserId)

	# get user's relationships
	relEndPoint = '/api/v1/relationships.json?access_token=' + oauthToken + '&user_id=' + selectedUserIdstr
	yamconn.request('GET', relEndPoint )

	# process son from yammer.com -> convert to python dict
	time.sleep(tdelay)
	relraw = yamconn.getresponse()
	relread = relraw.read()
	selectedRel = simplejson.loads(relread)

	# does the user have a superior?
	try:
		superiorId=selectedRel['superiors'][0]['id']
	except IndexError:
		superiorId = 'none'

	superiorIdstr=str(superiorId)

	if superiorIdstr != 'none':
		superiorCheck = 1
		supCount = 0
		for supUser in selectedRel['superiors']:
			supCount += 1
		print selectedEmail + ' has ' + str(supCount) + ' superior(s).'
	else:
		print selectedEmail + ' has no superiors.'

yamconn.close()