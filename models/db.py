# -*- coding: utf-8 -*-
count=0
i=0
paas='akash.d14@iiits.in:akash@210197'
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

#DAL(uri, migrate=False, fake_migrate=False)
#DAL(uri, migrate=False, fake_migrate=True)
#db=DAL('auth_user',migrate=False,fake_migrate=False)
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
#auth.define_tables()
############### Table for registration form ################
auth.settings.manager_actions = dict(db_admin=dict(role='admin',heading='Managing Registrations',tables=db.tables))
auth.settings.extra_fields['auth_user']=[
    Field('gender',requires=IS_IN_SET(['Male','Female'])),
    Field('room_partner',unique=True),
    #Field('room_alotted_or_not',requires=IS_IN_SET(['Yes','No'])),
    Field('phone_number',requires=IS_MATCH('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')),
    Field('physically_handicapped',requires=IS_IN_SET(['Yes','No'])),
    Field('admission_number'),
    #Field('which_hostel',requires=IS_IN_SET(['Boys Hostel','Girls Hostel'])),
    #Field('floor_no',requires=IS_IN_SET(['Ground','First','Second','Third','Fourth'])),
    Field('room_number',requires= [IS_INT_IN_RANGE(1,29) or IS_MATCH('^\d{1}([A-Z])')]),
    Field('type_of_account',requires=IS_IN_SET(['Student','Faculty','Hostel Committee','Super Admin']))]


#if db.auth_user.which_hostel=='Boys Hostel':
#    auth.settings.extra_fields['auth_user']=[Field('room_number')]
    #Field('which_hostel',requires=IS_IN_SET(['Boys Hostel','Girls Hostel'])),
    #Field('floor_no',requires=IS_IN_SET(['Ground','First','Second','Third','Fourth']))]
auth.define_tables(migrate=False)
#db.auth_user.email.requires=IS_EMAIL(forced='^.*\.in(|\..*)$')

db.auth_user.email.requires=IS_IIITS("iiits.in")
'''auth.settings.manager_actions = dict(
    db_admin=dict(role='Super', heading="Manage Database", tables=db.tables),
    content_admin=dict(role='Content Manager', tables=[content_db.articles, content_db.recipes, content_db.comments]),
    content_mgr_grp_v2 = dict(role='Content Manager v2', db=content_db,
        tables=['articles','recipes','comments'],
        smartgrid_args=dict(
                DEFAULT=dict(maxtextlength=50,paginate=30),
                comments=dict(maxtextlength=100,editable=False)
        )
    )
'''
###############################################################


## configure email
'''from gluon.tools import Mail
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'akash.d14@iiits.in'
mail.settings.login = paas

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
r=db().select(db.auth_user.registration_key,db.auth_user.first_name)
l=[]
for rs in r:
    if rs.registration_key!=' ':
        count+=1
        l.append(rs.first_name)
while(i<len(l)):        
    mail.send(to=['akash210197@gmail.com'],
    subject='Approve registration',
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
    message='To Approve registration of '+str(i)+' open link http://127.0.0.1:8000/welcome/appadmin/manage/db_admin')
    i+=1
    '''
#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
#db=DAL('sqlite://storage.sqlite')
############### Table for contact list ###############
db.define_table('contact',
                Field('name'),
                Field('phone'))
#db=DAL('sqlite://storage.sqlite')
######################################################


############### Table for image blog #################
db.define_table('image',
                Field('title',unique=True),
                Field('file1','upload'),
                format='%(title)s')
db.define_table('post',
                Field('image_id','reference image'),
                Field('author'),
                Field('email'),
                Field('body','text'))
db.image.title.requires=IS_NOT_IN_DB(db,db.image.title)
db.post.image_id.requires=IS_IN_DB(db,db.image.id, '%(title)s')
db.post.author.requires=IS_NOT_EMPTY()
db.post.email.requires=IS_EMAIL()
db.post.body.requires=IS_NOT_EMPTY()
db.post.image_id.writable=db.post.image_id.readable=False
############################################################



############# Table for Discussion forum ####################
db.define_table('db_topic',
                Field('topic_title',unique=True),
                Field('topic_doc','upload'))
db.define_table('db_change_room_services',
                Field('topic_subject',unique=True),
                Field('topic_document','upload'))
db.define_table('db_post',
                Field('discussion_id','reference db_topic'),
                Field('post_author'),
                Field('post_email'),
                Field('post_body','text'))
db.db_topic.topic_title.requires=IS_NOT_IN_DB(db,db.db_topic.topic_title)
db.db_post.post_author.requires=IS_NOT_EMPTY()
db.db_post.post_email.requires=IS_EMAIL()
db.db_post.discussion_id.writable=db.db_post.discussion_id.readable=False
###############################################################


########### Table for complaint register ###############
db.define_table('complaintregister',
                Field('complain_title'),
                #Field('Complained On','datetime'),
                Field('Complain_proofs','upload'),
                auth.signature)
db.complaintregister.complain_title.requires=IS_NOT_IN_DB(db,db.complaintregister.complain_title)


######################################################



######### Table for changing rooms #########
db.define_table('change_rooms',
                Field('name_of_room_changer','string',unique=True),
                Field('with_whom_you_want_to_change_with'),
                Field('with_whom_are_you_staying_with'),
                Field('why_do_you_want_to_change_your_room'),
                auth.signature)

#db.define_table('ch',
#               Field('change_rooms_id','reference change_rooms'))
#db.ch.change_rooms_id.readable=db.ch.change_rooms_id.writable=False
#db.change_rooms.name_of_room_changer.requires=IS_NOT_IN_DB(db,db.change_rooms.name_of_room_changer)
#############################################

############ Table for room partners #############
db.define_table('room_partner_list',
                Field('serial_number'),
                Field('room_partner_list_name'),
                Field('room_partner_name'))
#db.define_table('xyz',
#                Field('xyz_name'))
##################################################

########### Table for dashboard ####################
db.define_table('notice_board',
                Field('notice'),
                Field('notice_board_priority',requires=IS_IN_SET(['1','2','3','4','5'])))
'''from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
'''


########## Table to see whether a complaint resolved or not ####################
db.define_table('tell_outcome',
                Field('complain_id','reference complaintregister'),
                Field('problem_outcome',requires=IS_IN_SET(['Resolved','Not Resolved'])))
db.tell_outcome.complain_id.readable=db.tell_outcome.complain_id.writable=False
#################################################################################
########## Table to see whether request accepted or not #########################
db.define_table('tell',
                Field('request_id','reference change_rooms'),
                Field('request_outcome', requires=IS_IN_SET(['Accepted','Rejected'])))
db.tell.request_id.readable=db.tell.request_id.writable=False
#################################################################################
############################## Table for applying for leave ############################
db.define_table('leave_application',
                Field('reason_for_leave','text'),
                Field('leave_from','datetime'),
                Field('leave_upto','datetime'),
                auth.signature)
########################################################################################

############################### Table to see outcome ###################################
db.define_table('change_outcome',
                Field('change_id','reference change_rooms'),
                Field('tell_result',requires=IS_IN_SET(['Room Changed','Room not changed'])),
                Field('tt',default=0,readable=False,writable=False))
db.change_outcome.change_id.readable=db.change_outcome.change_id.writable=False
########################################################################################
db.define_table('oioi',Field('jjij'))
