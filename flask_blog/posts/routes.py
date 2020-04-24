from flask import render_template, url_for, flash, request, redirect, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)  # this uses the backref to the user db
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  # if doesn't exist it will return a get_or_404
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # No need to add here because we already have this in our db
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', legend='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted. We still hope to see more from you soon!', 'success')
    return redirect(url_for('main.home'))
