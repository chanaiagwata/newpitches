# from crypt import methods
from flask import render_template, request, redirect,url_for, abort
from . import main 
from ..models import Comments, User, Category, Pitch, Votes, Category
from ..import db
from . forms import Pitch_form, Category_form, Comment_form
from flask_login import login_required,current_user


#dynamic routing for the main page which displays pitch categories
@main.route('/')
def index():
    '''
    root page function
    '''
    category = Category.get_categories()
    
    title = 'Welcome to Pitch Factory'
    
    return render_template('index.html', title = title, categories = category)

#Aunthecation route that allow auntheticated users to submit new pitch
@main.route('/category/new-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    pitch = Pitch_form()
    category = Category.query.filter_by(id=id).first()
    
    if category is None:
        abort(404)   #404 status code returned if no user is found in database
        
    if pitch.validate_on_submit():
        content = pitch.Pitch_form.data
        new_pitch = Pitch(gist=content,categories_id= category.id,user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))
    title = 'New pitch'
    return render_template('new_pitch.html',title = title, Pitch_form = pitch, category=category)

#dynamic route for a view function that returns pitches for a particular category
@main.route('/category/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)
    pitches = Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)

#dynamic routing for creating new category
@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    form = Category_form()
    
    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_category() #save new category
        
        return redirect(url_for('.index'))
    title = 'Create new Category'
    return render_template('new_category.html', Category_form = form,title=title)

#dynamic routing for adding comment to a pitch
@main.route('/add_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def add_comment(id):
    form = Comment_form()
    title = 'Leave a comment about this pitch'
    pitches = Pitch.query.filter_by(id=id).first()
    
    if pitches is None:
        abort(404)
    if form.validate_on_submit():
        remark = form.remark.data
        new_comment = Comments(remark = remark, user_id = current_user.id, pitches_id = pitches.id)
        new_comment.save_comment() #save the new comment
        return redirect(url_for('.new_pitch', id=pitches.id))

    return render_template('add_comment.html', title=title, comment_form=form)
        
    
    
#dynamic routing for viewing each pitch with its comments
@main.route('/pitch_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def pitch_comment(id):
    print(id)
    pitches = Pitch.query.get(id)    
    title = 'Latest comments'
    if pitches is None:
        abort(404)
    comment = Comments.get_comments(id)
    return render_template('pitch_comment.html', title=title, pitches=pitches, comment=comment)
         