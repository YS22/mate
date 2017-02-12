# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid,models
from forms import LoginForm
from models import User
from forms import LoginForm,RegistrationForm,InfoForm,EstablishForm,JoinForm,IndexForm
from models import User, Role,Group
from datetime import datetime



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login(): 
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is not None and user.password==form.password.data:
            login_user(user, form.remember_me.data)
            return redirect(url_for('index'))
           
        flash(u'密码或用户名错误!')
    return render_template('login.html', form=form)


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    role_list=[]
    ren_lenth=0
    form = IndexForm()
    zu = Group.query.filter_by(groupname=form.name.data).first()
    if form.validate_on_submit():
        if zu is None :
            flash(u'此群未建立！')
        else:
             ren_list=zu.user.all()
             ren_lenth=len(ren_list)
             if g.user in ren_list:
                for rens in ren_list:
                    
                    # if g.user.role is  None:
                    #     flash(u'请编辑你的信息再操作！')
                    #     return redirect(url_for('index'))

                    # else:
                    role_list.append(rens.role[0])
                   
             else:
                flash(u'你不属于该群成员！')
                return redirect(url_for('index'))   
        # if zu is None :
        #      flash(u'此群未建立！')          
             # for rens in ren_list:
             #    role_list.append(rens.role[0])
                
    group_list= g.user.group.all()
    # role_list= models.Role.query.all()##该群所有的用户角色集合
    position_list=[]
    name_list=[]
    tel_list=[]
    for role in role_list:
        position_list.append(role.position)
        name_list.append(role.name)
        tel_list.append(role.tel)
    return render_template('index.html',
                           title='Home',
                           form=form,
                           position_list=position_list,name_list=name_list,tel_list=tel_list,role_list=role_list,group_list=group_list,zu=zu,ren_lenth=ren_lenth)

    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'注册成功，请登录！')
        
        return redirect(url_for('login'))
    if User.query.filter_by(nickname=form.nickname.data).first():
        flash(u'用户名已注册')
    return render_template('register.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = InfoForm()
    role = Role.query.filter_by(name=form.name.data).first()
    if form.validate_on_submit():
         
        if role is None:  
            roles= Role(position=form.position.data,name=form.name.data,tel=form.tel.data,author=g.user)
            db.session.add(roles)
            db.session.commit()
            flash(u'信息添加成功！')
        else:
            if  g.user.role[0].name==role.name:
                role.position=form.position.data
                role.tel=form.tel.data
                db.session.add(role)
                db.session.commit()
                flash(u'信息修改成功！')
            else:
                flash(u'真实姓名不符，无法修改！')

    role_list= models.Role.query.all()
    position_list=[]
    name_list=[]
    tel_list=[]
    positions=[]
    names=[]
    tels=[]
    for role in role_list:
        position_list.append(role.position)
        name_list.append(role.name)
        tel_list.append(role.tel)
    
    return render_template('edit.html',
                           title='Home',
                           form=form,
                           position_list=position_list,name_list=name_list,tel_list=tel_list,role_list=role_list)


@app.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    form = EstablishForm()
    if form.validate_on_submit():
        l = Group.query.filter_by(groupname=form.name.data).first()
        if l is None:
            group = Group(groupname=form.name.data)
            db.session.add(group)
            db.session.commit()
            flash(u'创建成功，快加入该群吧！')
            return redirect(url_for('join'))

        else:
            flash(u'该名称已被占用！')

        
    return render_template('group.html', form=form)

@app.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    form = JoinForm()
    if form.validate_on_submit():
        s = Group.query.filter_by(groupname=form.name.data).first()
        if s is None:
            flash(u'此群未建立')
        else:
            ren_list=s.user.all()
            for ren in ren_list:
                if ren==g.user:
                    flash(u'你在该组群，不需重新加入！')
                    return redirect(url_for('join'))
            else:
                g.user.group.append(s)
                db.session.add(g.user)
                db.session.commit()
                flash(u'加入成功！')					
            
    return render_template('join.html', form=form)

@app.route('/groupinfo', methods=['GET', 'POST'])
@login_required
def groupinfo():
    role_list=[]
    group_list=g.user.group.all()
    for group in group_list:
        ren_list=group.user.all()
        for ren in ren_list:
            role_list.append(ren.role[0]) 
    group_lenth=len(group_list)                                                                                                          
    return render_template('groupinfo.html',group_list=group_list,role_list=role_list,group_lenth=group_lenth)
	




