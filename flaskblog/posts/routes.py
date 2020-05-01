 
from flask import (render_template,url_for,
                    flash,redirect,request,abort,Blueprint)
from flask_login import current_user,login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm


posts=Blueprint('posts',__name__)

# posts = [
#     {
#         'auther': 'najah said',
#         'title': 'Blog post 1',
#         'content': 'First Post content',
#         'date_posted': 'April 19, 2020'
#     },
#     {
#         'auther': 'najah said',
#         'title': 'Blog post 2',
#         'content': 'Second Post content',
#         'date_posted': 'April 21, 2020'
#     },
#     {
#         'auther': 'najah said',
#         'title': 'Blog post 3',
#         'content': 'Third Post content',
#         'date_posted': 'April 22, 2020'
#     }
# ]



@posts.route('/posts/create',methods=['GET','POST'])
@login_required
def add_post():
    form=PostForm()
    if form.validate_on_submit():
        flash('Add Post Success Created !','success')
        post =Post(title=form.title.data,content=form.content.data,auther=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('posts/create.html',title="create Post",form=form)

@posts.route('/posts/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('posts/post.html',title=post.title,post=post)

@posts.route('/posts/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.auther !=  current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Updated Post Success!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('posts/create.html',title="update Post",form=form,legend="Update Form")

@posts.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id): 
    post=Post.query.get_or_404(post_id)
    if post.auther !=  current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit( )
    flash('Deleted Post Success!','success')
    return redirect(url_for('main.index'))
   
