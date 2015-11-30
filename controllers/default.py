# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
#    if not session.counter:
   #     session.counter=1
    session.counter=(session.counter or 0)+1
    response.flash = T("Welcome")
    y={}
    y['title']=[]
    count=0
    for row in db(db.notice_board.notice_board_priority<=5).select(orderby=db.notice_board.notice_board_priority):
        count+=1
        x=row.notice
        if count<=5:
            y['title'].append(x)
        else :
            y['title'][count-6]=x
            #count=5
    return dict(message="Welcome to Our Hostel Management Portal!",counter=session.counter,y=y)
#@auth.requires_permission('read','person')

def first():
    if request.vars.visitor_name:
        session.visitor_name=request.vars.visitor_name
        redirect(URL('second'))
    return dict()

def second():
    return dict()

@auth.requires_login()
def p1():
        return dict()

def p2():
        return dict()

def p3():
        return dict()

def p4():
        return dict()

@auth.requires_login()
def ak():
    form = SQLFORM(db.image,user_signature=True).process()
    images = db().select(db.image.ALL, orderby=db.image.title)
    return locals()

@auth.requires_login()
def dis():
    form = SQLFORM(db.db_topic).process()
    get_db_topics = db().select(db.db_topic.ALL, orderby=db.db_topic.topic_title)
    return locals()

@auth.requires_login()
def complain():
    form = SQLFORM(db.complaintregister).process()
    complaints = db().select(db.complaintregister.ALL,orderby=db.complaintregister.complain_title)
    return locals()


@auth.requires_login()
def show_complain():
    complaintregister = db.complaintregister(request.args(0,cast=int)) or redirect(URL('index'))
    db.complainpost.complain_id.default = complaintregister.id
    form=SQLFORM(db.complainpost)
    if form.process().accepted:
        response.flash='your complaint is posted'
    comments = db(db.complainpost.complain_id==complaintregister.id).select()
    return locals()

@auth.requires_login()
def show2():
    db_topic = db.db_topic(request.args(0,cast=int)) or redirect(URL('index'))
    db.db_post.discussion_id.default = db_topic.id
    form=SQLFORM(db.db_post)
    if form.process().accepted:
        response.flash='your comment is posted'
    comments = db(db.db_post.discussion_id==db_topic.id).select()
    return dict(form=form, comments=comments, db_topic=db_topic)

@auth.requires_login()
def show():
    image = db.image(request.args(0,cast=int)) or redirect(URL('index'))
    db.post.image_id.default = image.id
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'Your comment is posted'
    comments = db(db.post.image_id==image.id).select()
    #return dict(image=image, comments=comments, form=form)
    return locals()

def download():
    return response.download(request, db)

def show3():
    change_rooms=db.change_rooms(request.args(0,cast=int)) or redirect(URL('index'))
    #change_rooms = db.change_rooms(request.args(0,cast=int)) or redirect(URL('index'))
    db.ch.change_rooms_id.default=change_rooms.id
#    name=db.change_rooms(change_rooms_id).name_of_room_changer
    return dict(change_rooms=change_rooms)

def account_details():
    #name=db.auth_user.first_name
    if auth.is_logged_in():
        account_type=db.auth_user(auth.user_id).type_of_account
        account_name=db.auth_user(auth.user_id).first_name
        account_lastname=db.auth_user(auth.user_id).last_name
        account_admission_number=db.auth_user(auth.user_id).admission_number
        account_email=db.auth_user(auth.user_id).email
        account_room_number=db.auth_user(auth.user_id).room_number
        account_room_partner=db.auth_user(auth.user_id).room_partner
    return dict(account_type=account_type,account_name=account_name,account_lastname=account_lastname,account_admission_number=account_admission_number,account_email=account_email,account_room_number=account_room_number,account_room_partner=account_room_partner)

def display_form():
    form=FORM('Your name:',
              INPUT(_name='name',requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        response.flash='form accepted'
    elif form.errors:
        response.flash='form has errors'
    else:
        response.flash='please fill the form'
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0)=='profile':
        db.auth_user.type_of_account.writable=False
        db.auth_user.registration_key.readable=db.auth_user.registration_key.writable=False
        #db.auth.settings.remember_me_form.readable=db.auth.settings.remember_me_form.writable=False
    return dict(form=auth())

@auth.requires_membership('manager')
def manage():
    grid = SQLFORM.smartgrid(db.image,linked_tabled=['post'])
    return dict(grid=grid)
'''@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
'''

def wiki1():
    return auth.wiki()

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
@auth.requires_login()
def contacts():
    grid=SQLFORM.grid(db.contact,user_signature=True)
    #db.contact.csv.readable=db.contact.csv.writable=False
    if auth.is_logged_in() and db.auth_user(auth.user_id).type_of_account=="Hostel Committee":
        return dict(grid1=grid)
def contactlist():
    y={}
    y['name']=[]
    y['no']=[]
    for row in db(db.contact._id>0).select():
        x=row.name
        y['name'].append(x)
        z=row.phone
        y['no'].append(z)
    return dict(y=y) 
def list():
    #if auth.is_logged_in() and db.auth_user(auth.user_id).type_of_account=='Super Admin':
    y={}
    y['name']=[]
    y['room_partner_name']=[]
    y['serial']=[]
    for row in db(db.room_partner_list._id>0).select():
        x=row.room_partner_list_name
        y['name'].append(x)
        z=row.room_partner_name
        y['room_partner_name'].append(z)
        u=row.serial_number
        y['serial'].append(u)
    return dict(y=y)

def notice():
    form=SQLFORM(db.notice_board).process()
    if form.accepted:
        response.flash= 'Notice Uploaded'
    return dict(form=form)

def seelist():
    return dict()

def tell_outcome():
    complaintregister = db.complaintregister(request.args(0,cast=int)) or redirect(URL('index'))
    rt=complaintregister.id
    db.tell_outcome.complain_id.default = complaintregister.id
    if db.auth_user(auth.user_id).type_of_account=="Hostel Committee":
        form=SQLFORM(db.tell_outcome).process()
        if form.accepted:
            response.flash = 'Outcome Given'
        return dict(form=form)
    #if auth.is_logged_in() and db.auth_user(auth.user_id).type_of_account=="Student":
    else:
        flag=0
        result1=db().select(db.tell_outcome.ALL)
        for a in result1:
            if rt==a.complain_id:
                flag=1
                break
        if flag==1:
            result=db.tell_outcome(db.tell_outcome.complain_id==complaintregister.id)
            out=result.problem_outcome
        else:
            out="Not Resolved"
        return dict(out=out)


def change_outcome():
    w=[]
    w1=[]
    change_rooms = db.change_rooms(request.args(0,cast=int)) or redirect(URL('index'))
    db.change_outcome.change_id.default = change_rooms.id
    if db.auth_user(auth.user_id).type_of_account=="Hostel Committee":
        form=SQLFORM(db.change_outcome).process()
        if form.accepted:
            response.flash = "Response Given"
            #db.change_outcome.update_or_insert(change_id=change_rooms.id,tt=1)
        return dict(form=form)
    #db.change_outcome.update_or_insert(change_id=change_rooms.id,tt=0,tell_result="Not Yet Finalised")
    if ((db.auth_user(auth.user_id).type_of_account=="Student" or db.auth_user(auth.user_id).type_of_account=="Super Admin")):
        flag=0
        qw=change_rooms.id;
        w2=db().select(db.change_outcome.ALL)
        for w in w2:
            if qw==w.change_id:
                flag=1
                break
    
        if flag==1:
            o1=db.change_outcome(db.change_outcome.change_id==change_rooms.id).tell_result
        else:
            o1="Not Yet Finalised"
   
        return dict(o1=o1)
        


@auth.requires_login()
def changing():
    form=SQLFORM(db.change_rooms).process()
    changes=db().select(db.change_rooms.ALL,orderby=db.change_rooms.name_of_room_changer)
    return locals()

def tell():
    #change_rooms = db.change_rooms(request.args(0,cast=int)) or redirect(URL('index'))
    #db.tell.request_id.default = change_rooms.id
    if db.auth_user(auth.user_id).type_of_account=="Hostel Committee":
        form=SQLFORM(db.tell).process()
        if form.accepted:
            response.flash = 'Result Given'
        return dict(form=form)
    '''if auth.is_logged_in() and db.auth_user(auth.user_id).type_of_account=="Student":
        result1=db.tell(db.tell.request_id==change_rooms.id)
        out=result1.request_outcome
        return dict(out=out)
    '''

def leave():
    n=[]
    m=[]
    form=SQLFORM(db.apply_leave).process()
    if form.accepted:
        row=db().select(db.apply_leave.ALL)
        we=row.last().id
        w1=row.last().leave_from
        y=row.last().leave_upto
        w=y-w1
        #for rows in w1:
        #    w.append(rows.leave_from)
        #y=db.apply_leave(id).leave_upto
        #n=w.split('-')
        #m=y.split('-')
        if(w.days>=0):
            response.flash='Leave Submitted'
        #return dict(w=w)
        else:
            response.flash='Leave Not Submitted'
            db(db.apply_leave.id==we).delete()
    return dict(form=form)
'''def see_outcome():
    if auth.is_logged_in() and db.auth(auth.user_id).type_of_account=="Student":
        n=db(db.tell_outcome._id>0).select()
        result=db.tell_outcome.problem_outcome
        return dict(result=result,n=n)
'''
def send_mail():
    count=0
    i=0
    r=db().select(db.auth_user.registration_key,db.auth_user.first_name)
    l=[]
    for rs in r:
        if rs.registration_key!=' ':
            count+=1
            l.append(rs.first_name)
    while(i<count):
        mail.send(to=['akash210197@gmail.com'],
        subject='Approve registration',
            # If reply_to is omitted, then mail.settings.sender is used
            #reply_to='us@example.com',
        message='To Approve registration of '+l[i]+' open link http://127.0.0.1:8000/welcome/appadmin/manage/db_admin')
        i+=1
