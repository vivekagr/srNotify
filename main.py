#!/usr/bin/env python

# This script looks up /r/gamedeals/new every 120 seconds and pushes the notification
# for new posts to Growl app on Mac OS

# Uses PRAW - https://github.com/praw-dev/praw (for easy access to Reddit API)
# and GNTP - https://github.com/kfdm/gntp (for pushing Growl notification)

import gntp.notifier
import praw
import time
import sys

# icon for use with growl notification
ICON_URL = "http://i.imgur.com/8CTk6.png"
# user agent to be used by PRAW
USER_AGENT = 'new /r/gamedeals notifier by & for /u/mpheus'

growl = gntp.notifier.GrowlNotifier(
    applicationName = "/r/gamedeals notifier",
    notifications = ["New Deal"],
    defaultNotifications = ["New Deal"],
)
growl.register()

r = praw.Reddit(user_agent=USER_AGENT)

already_done = [] # for storing the uids of posts already notified
first_time = True

while True:
	try:
		data = r.get_subreddit('gamedeals').get_new_by_date(limit=10)
		for x in data:
			if x.id not in already_done:
				# so that notification remains on the screen until closed
				stick = False if first_time else True
				# sending growl notification
				growl.notify(
					noteType = "New Deal",
					title = x.domain,
					description = x.title,
					icon = ICON_URL,
					sticky = stick,
					priority = 1,
					callback = x.permalink
					)
				# adding uid of the post to already_done list
				already_done.append(x.id)
				print "Notified about", x.title, "at", time.strftime("%d %b - %I:%M:%S %p")
		print "Last checked for game deals at", time.strftime("%d %b - %I:%M:%S %p")
		time.sleep(120)
		first_time = False
	
    # We want the script to run endlessly so we catch all the exceptions and then put the
    # script to sleep for 120 seconds. Exceptions mostly occur due to not being able to reach
    # the host.
    
	except Exception, e:
		print "Error " + str(e) + " caught at " + time.strftime("%d %b - %I:%M:%S %p")
		time.sleep(120)