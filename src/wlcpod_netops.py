#! /usr/bin/python
"""
WLCP network functions defined here:

cpod_login(email, password, language='chinese')
get_html(document_url, localname=None, data=None)
download_file(lessondir, lesson_name, name, url, already_existing_files, valid_names = None)
"""

import re
import urllib, urllib2
import socket
import time, os, sys

char_state = None

def cpod_trad():
	"""switch to traditional characters"""

	global char_state

	if char_state is 'trad':
		return

	char_state = 'trad'
	try:	# CPod servers are a bit funky, so an exception's always thrown
		urllib2.urlopen('http://chinesepod.com/lessons/setting?ctype=2&chars=1')
	except:
		pass

def cpod_simp():
	"""switch to simplified characters"""

	global char_state

	if char_state is 'simp':
		return

	char_state = 'simp'
	try:	# CPod servers are a bit funky, so an exception's always thrown
		urllib2.urlopen('http://chinesepod.com/lessons/setting?ctype=1&chars=1')
	except:
		pass

def cpod_login(email, password, language='chinese'):
	"""logins in the chinesepod.com website and installs a
	urllib opener object for premium content downloading"""

	# create web page opener
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	urllib2.install_opener(opener)

	# retrieve login page to get the authenticity token	
	print 'Opening Praxis login page...'
	login_page = get_html(u'https://secure.praxislanguage.com/accounts/login?service=' + language + u'pod&force=&continue=http%3A%2F%2F' + language + u'pod.com%2Flogin')

	prefix = u'name="authenticity_token" type="hidden" value="'
	authenticity_token = re.search(prefix + '(?P<token>.*?)"', login_page).group('token')

	# log in
	print 'Logging into account %s...' % email
	logged_in_page = get_html(u'https://secure.praxislanguage.com/accounts/login?service=' + language + u'pod&force=&continue=http%3A%2F%2F' + language + u'pod.com%2Flogin', data = urllib.urlencode({u'user_email':email, u'user_password':password, u'authenticity_token':authenticity_token}))

	if 'Signout' in logged_in_page:
		print 'Successfully logged in!'
	else:
		print 'WARNING: unable to log in! (please check your login information)'
		print 'WLCP is aborting.'
		time.sleep(3)
		sys.exit()

	# account for flaky Internet; for some reason, this isn't as important
	# for logging in (even when chinesepod.com is slow) as for downloading
	# bigger files
	socket.setdefaulttimeout(5)

	#get_html('http://chinesepod.com/lessons/setting/')

def get_html(document_url, localname=None, data=None, ctype=None):
	"""download a file from ChinesePod via a premium account;
	this function attempts to recover from network errors,
	makes use of a local cache and returns file contents"""

	if localname <> None:
		# check for local file
		try:
			input = open(localname, 'r')
			document_html = unicode(input.read(), 'utf-8')
			input.close()
			return document_html

		except IOError: pass

	# set character type
	if ctype is 'trad':
		cpod_trad()
	if ctype is 'simp':
		cpod_simp()

	try_again = True
	while try_again:
		try_again = False
		try:
			response = urllib2.urlopen(document_url, data=data)
			document_html = unicode(response.read(), 'utf-8')
			response.close()

		except socket.timeout:
			print "ERROR: socket timed out; trying again"
			time.sleep(5)
			try_again = True

		except urllib2.URLError, e: # urllib2.URLError: <urlopen error timed out>
			if "HTTP Error 403" in str(e):
				print "ERROR: HTTP Error 403 retrieving: " + document_url + " (skipping...)"

				return None

			if "HTTP Error 404" in str(e):
				print "ERROR: HTTP Error 404 retrieving: " + document_url + " (skipping...)"
				return None

			print "ERROR: problem opening URL:" + document_url + ": " + str(e)
			if localname <> None:
				print "(local filename: " + localname + ")"

			if hasattr(e, 'reason'):
				'failed to reach a server; reason: ', e.reason
			elif hasattr(e, 'code'):
				'server couldn\'t fulfill the request; error code: ', e.code
			print "trying again in 5 seconds..."

			time.sleep(5)

			try_again = True

	if localname <> None:
		output = open(localname, 'w')
		output.write(document_html.encode('utf-8'))
		output.close()

	return document_html

def download_file(lessondir, lesson_name, name, url, already_existing_files, valid_names = None):
	"""use for downloading a file via urlretrieve; this function attempts
	to recover from network errors and does not return file contents"""

	if name in already_existing_files:
		print "\t%s: already downloaded (skipping)" % name
		if valid_names <> None:
			valid_names.append(name)

		return

	print "\t%s: downloading..." % name

	try_again = True
	while try_again:
		try_again = False
		try:
			urllib.urlretrieve(url, os.path.join(lessondir, lesson_name) + u'/' + name)
			if valid_names is not None:
				valid_names.append(name)

		except socket.timeout:
			print "ERROR: socket timed out; trying again"
			time.sleep(5)
			try_again = True

		except urllib2.URLError, e: # urllib2.URLError: <urlopen error timed out>
			if "HTTP Error 403" in str(e):
				print "ERROR: HTTP Error 403 retrieving: " + document_url + " (skipping)"

				return

			print "ERROR: problem opening URL:" + document_url + ": " + str(e)
			if localname <> None:
				print "(local filename: " + localname + ")"

			if hasattr(e, 'reason'):
				'failed to reach a server; reason: ', e.reason
			elif hasattr(e, 'code'):
				'server couldn\'t fulfill the request; error code: ', e.code
			print "trying again in 5 seconds..."

			time.sleep(5)

			try_again = True

		except urllib.ContentTooShortError:
			print u'ERROR: retrieved data was not completely downloaded'

			# this shouldn't happen
			sys.exit()

		except IOError, (errno, strerror):
			print u'ERROR: unable to download ' + url + u' to folder ' + os.path.join(lessondir, lesson_name)

			if "timed out" in strerror:
				print u'socket timed out; trying again...'
				time.sleep(5)
				try_again = True

			elif errno <> 2:
				print IOError(errno, strerror) 

			# this shouldn't happen, either
			if not try_again:
				sys.exit()
