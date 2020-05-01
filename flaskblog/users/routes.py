from flask import render_template,url_for,flash,request,redirect, Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from flaskblog import db ,bcrypt
from flaskblog.models import User,Post
from flaskblog.users.forms import (RegistrationForm,LoginForm,UpdateAccountForm,
                                        RequestResetForm,ResetPasswordForm)
from flaskblog.users.utils import save_picture,send_reset_email
users=Blueprint('users',__name__)





@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account Has been created . Please Login  ', 'success')
        return redirect(url_for('users.login'))
    return render_template('pages/register.html', form=form)






@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@blog.com' and form.password.data == '12345678':
        #     flash('Login with Success!', 'success')
        #     return redirect(url_for('index'))
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash('Login with Success!', 'success')
            return redirect(next_page) if next_page else  redirect(url_for('main.index'))

        else:
            flash(' UnSuccess login! Please Check Email & Password and Try again', 'danger')
    return render_template('pages/login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@users.route('/account', methods=['GET', 'POST'])
@login_required 
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data )
            current_user.image_file=picture_file 
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Update Success!', 'success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('pages/account.html',image_file=image_file,form=form)




@users.route('/user/<string:username>')
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(auther=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page ,per_page=5) 
    return render_template('pages/user_posts.html', posts=posts,user=user)



 
@users.route('/forgetpassword', methods=['GET', 'POST']) 
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email Has Been Sent to Reset Password!','info')
        return redirect(url_for('users.login'))
    return render_template('reset/request_reset_password.html',title="Reset Password",form=form,legend="Reset Password")






@users.route('/newpassword/<token>',methods=['GET', 'POST']) 
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('Invalid Token or Exprired Token Please Request Again','warning')
        return redirect(url_for('users.request_reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash('Update password Successfully . Please Login  ', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset/reset_password.html',title="New Password",form=form,legend="New Password")
