Chaperone App
=============

The chaperone app was created to replace an existing system for managing school
events and their volunteers.

Event listings page and Event pages
--------------------------

There is an event listings page that lists all of the future events in order of
which one is most close to taking place. Users can click on an event and
be taken to that event's corresponding page.

There, users will be able to see
things like the event's date, time, description, administrator, administrator
contact information, notes from the administrator or from other volunteers, a
list of other volunteers, contact info of other volunteers, and how many
volunteers are still needed.

Additionally, users can sign up or unsign up for that particular event on that
page.

Types of users in the chaperone app
-----------------------------------

There are 2 main types of regular users in this app:
    * Event Administrators
    * Chaperones

Site Administrators
*******************

These are the people in the activities office who are going to be creating the
events and designating who is the event administrator.


Event Administrators
********************

Each event has a single **event administrator**, that is set initially by the site
administrator that created the event. This can be changed by a site admin
later.

There is a restricted group of users who are allowed to be event administrators.

Any site administrator can add or remove users from this group.

**This is a Django group and LDAP Security group, and it is called "Intranet_Event_Admin". If the database is
ever reset, this group needs to be re-created manually through the admin page
verbatim or a user who belongs to this security group needs to log in.
If not, the "Add a new event" page will not work**

The event admin's contact info will be posted on the event's description page,
as well as a list of all of the other users who have signed up for the event.
This is safe, because only logged-in users can see this information.

Event administrators can
  * Send emails to the whole BBHS faculty to request volunteers (through a site
    admin)
  * Send email reminders to the event's signed up users (through a site admin)
  * Read the public notes and the private notes that users post on the event's
    page
  * Sign up other users directly for the event
  * Remove other volunteers from the event's registration

Regular users
*************

Most users in the system will be placed here. The regular user will be able to
view all future events, and will be able to sign up or unsign up for events.

The events have a weight system. Every teacher has a fixed yearly requirement.
At the time of writing, that requirement was 4 event units per year.
Each event has it's own weight. For example, Kairos might be worth three event
units since it takes place over three days.

Every time a user signs up for an event, his or her required chaperone event
count will be decreased by that event's corresponding weight. Likewise, when a user unsigns up, the count will
increment by that weight.

If a user goes past his or her requirement count, it will appear as if the user
has reached a plateau of 0 required events, but the application is behind the
scenes
going into negative numbers in case that data is ever desired.

Additionally, every time a user signs up for or unsigns up for an event, the
action, date and time are logged in the database.

Markdown rendering for event descriptions
-----------------------------------------

When a user adds an event with the custom form, they get the option to use
markdown rendering.

Markdown is a powerful text-to-HTML conversion tool for web writers. Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML).

This document that I wrote is written using a similar text-to-HTML conversion tool called
restructured text. It's more confusing, don't look at the source. Check out the
links below instead.

Here is a good example article written in markdown:

http://daringfireball.net/projects/markdown/

A cheat sheet:

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

Yearly Deadline
---------------

On the deadline date, it will check for those who missed the deadline and let
the interested parties know.

At the beginning of the school year, it will reset all the yearly counts
(events done so far, events still needed).

The correct dates need to be updated in ~/bbhs_intranet/bbhs/settings.py at the
very bottom. The years need to be incremented by 1 every year.

It will send the ADMINS in the settings.py file email reminders when this is
necessary.

Emails
------

The chaperone system will send out a variety of emails automatically.

Every month, it will go through the system and send an email reminder to all of
the members of the Intranet_Chaperone security group that still haven't
fulfilled their requirement.

Every day, it will go through all of the events that are happening with 2 days,
and let the registered volunteers have an email reminder

When a user signs up for an event, it will email the event administrator
letting them know who signed up, and it will send the user who signed up an
email confirmation.

Once a year, it will send an email to the site admins (Michael, David, Luis)
with instructions on how to update the start school date and the end school
date so it knows when the chaperone deadline is, and when to reset the user's
yearly event counts.

Once a year, it will also send an email to the designated DEADLINE_EMAIL
variable defined in ~/bbhs_intranet/bbhs/settings.py letting them know what
users missed the deadline for required events.
