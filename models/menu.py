# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(B('IIIT','Sricity'),XML('&trade;&nbsp;'),
#                  _class="navbar-brand",_href="http://www.iiits.ac.in/",
#                  _id="iiits-logo")
response.logo = A(IMG(_src=URL('static', 'iiits-logo.png'),
                      _height="55px"),_href="http://www.iiits.ac.in/",_id="iiits-logo")
#response.title=settings.title()
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new portal'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
]

if 1==1:
    response.menu += [
        (T('Our Hostel'), False, URL('welcome', 'default', 'wiki1')),
        (T('Emergency Numbers'),False,URL('welcome','default','contactlist')),
          (T('Facilities'), False, '#', [
              (T('Room Changing/Swapping'), False,
               URL(
               'welcome', 'default', 'changing' )),
              (T('Room Allotment List'), False,
               URL(
               'welcome', 'default', 'list')),
              (T('Hostel structure'), False,
               URL(
               'welcome' , 'default', 'p5')),
              (T('Complaints and Suggestions'),False,
               URL(
               'welcome' , 'default' , 'complain' )),
              (T('Images'),False, URL(
                'welcome', 'default' , 'ak' )),
              (T('Our Discussion Forum'),False,URL(
                'welcome','default','dis')),
              (T('About'), False, URL(
               'welcome', 'default', 'about')),
              ])]
if auth.is_logged_in():
    response.menu=response.menu+[(T('Leave Form'),False,URL('welcome','default','leave'))]
if auth.is_logged_in() and db.auth_user(auth.user_id).type_of_account=='Hostel Committee':
    db.auth_user.registration_key.writable=db.auth_user.registration_key.readable=True
    #db.auth_groups.readable=db.auth_groups.writable=False
    response.menu+= [(T('Hostel Admin'), False, None,[
                      (T('Manage Users'),False,URL('appadmin','manage',args=['db_admin'])),
#if auth.is_logged_in() and (db.auth_user(auth.user_id).type_of_account=='Hostel Committee' or db.auth_user(auth.user_id).type_of_account=='Super Admin'):
#    response.menu=response.menu+[(T('Allotments'),False,URL('welcome','default','list'))]
#if auth.is_logged_in() and (db.auth_user(auth.user_id).type_of_account=='Hostel Committee' or db.auth_user(auth.user_id).type_of_account=='Super Admin'):
                      (T('Notice'),False,URL('welcome','default','notice'))])]
if auth.is_logged_in() and db.auth_user(auth.user_id).type_of_account=='Super Admin':
    response.menu+=[(T('Super Admin Interfaces'),False,None,[
                        (T('Databases'),False,URL('welcome','appadmin','index')),
                        (T('Edit Website'),False,URL('admin','default','site'))
                        ])]
if auth.is_logged_in():
    response.menu=response.menu+[(T('Account'),False,URL('welcome','default','account_details'))]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################


if "auth" in locals(): auth.wikimenu()
