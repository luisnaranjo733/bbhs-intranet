import os
import sys
sys.path.append('/home/luis/bbhs_intranet/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from bbhs.settings import startOfYear, endOfYear, OBLIGATION_NUMBER,
sendTextEmail, DEADLINE_EMAIL, ADMINS
from intranet.models import UserProfile


for profile in UserProfile.objects.all():
    if not profile.user.is_active:
        continue


    print 'Resetting', profile
    profile.eventsNeeded = OBLIGATION_NUMBER
    profile.eventsDoneSoFar = 0
    profile.save()

msg = '''
Hello %s!

This is the BBHS Intranet and I've got an important message for you.

Today is the day.
I just reset everybody's eventsNeeded count to the OBLIGATION_NUMBER in the
settings file and the eventsDoneThisYear count to 0.

I need you to go edit ~/bbhs_intranet/bbhs/settings.py

At the very bottom, increment the year by one for both variables (endOfYear and startOfYear).

Then, reset apache.

Thanks! See ya in a year.
'''

for username, email in ADMINS:
    a = msg % username
    sendTextEmail(msg, 'CRITICAL INTRANET REMINDER', email)

# cron jobs

# 0 0 1 7 * /path/to/script
# July 1 - deadline for obligation

# 0 0 1 9 * /path/to/script
# September 1 - reset events needed
