# Created by Neil McCarthy, Implementation Engineer, Yammer, nmccarthy-inc@yammer.com
# v0.1, 04/20/2011

import sys, httplib, simplejson, csv, time

# here is the oath token, replace it with your own
oauthToken = 'todo'
csvFilename = 'todo.csv'

# time delay to prevent rate limiting
tdelay=0

emailList = csv.reader(open(csvFilename, 'rb'), delimiter=',')

for row in emailList:
	# initiate connection to Yammer (must be https)
	yamconn = httplib.HTTPSConnection("www.yammer.com")

	selectedEmail = row[0]

	# find user by email address so we can get their id
	findEndPoint='/api/v1/users/by_email.json?access_token=' + oauthToken + '&email=' + selectedEmail
	yamconn.request('GET', findEndPoint)

	# process json from yammer.com -> convert to python dict
	time.sleep(tdelay)
	userraw = yamconn.getresponse()
	userread = userraw.read()
	selectedUser = simplejson.loads(userread)

	# get the id of the user
	try:
		selectedUserId = selectedUser[0]['id']
	except IndexError:
		print selectedEmail + ' does not exist.'
		continue

	selectedUserIdstr = str(selectedUserId)

	yamconn.close()

	superiorIdstr = 'first'

	while superiorIdstr != 'none':
		yamconn = httplib.HTTPSConnection("www.yammer.com")

		# get user's relationships
		relEndPoint = '/api/v1/relationships.json?access_token=' + oauthToken + '&user_id=' + selectedUserIdstr
		yamconn.request('GET', relEndPoint )

		# process son from yammer.com -> convert to python dict
		time.sleep(tdelay)
		relraw = yamconn.getresponse()
		relread = relraw.read()
		selectedRel = simplejson.loads(relread)

		try:
			superiorId=selectedRel['superiors'][0]['id']
		except IndexError:
			print selectedEmail + ' has no superiors.'
			superiorId = 'none'

		superiorIdstr=str(superiorId)

		# delete user's superior
		if superiorIdstr != 'none':
			delEndPoint = '/api/v1/relationships/' + superiorIdstr + '.json?access_token=' + oauthToken + '&user_id=' + selectedUserIdstr + '&type=superior'
			yamconn.request('DELETE', delEndPoint)
			time.sleep(tdelay)
			deleteTest=yamconn.getresponse()
			if deleteTest.status == 200:
				print selectedEmail + ': superior was removed.'
			else:
				print selectedEmail + ': something went wrong. ' + str(deleteTest.status) + ' ' + str(deleteTest.reason) + '' + delEndPoint
		yamconn.close()

	yamconn.close()

yamconn.close()