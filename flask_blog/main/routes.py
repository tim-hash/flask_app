from flask import render_template, request, Blueprint
from flask_blog.models import Post


main = Blueprint('main', __name__)

# Route will allow us to create the different page
@main.route('/')  # Root page
@main.route('/home')  # can have multiple route to lead to same page ie handled by same functions
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # Now we can use template to print html page using this render_template
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():  # always need to change the function as well
    return render_template('about.html', title='About')
