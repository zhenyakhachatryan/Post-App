from flask import Flask,request,render_template,flash,redirect,url_for,session
from flask_login import current_user,login_user,logout_user,LoginManager,login_required
from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy.orm import joinedload
from models import db,USER,POST,COMMENT,LIKE
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


app=Flask(__name__,template_folder='templates')
app.config.from_pyfile('config.py')
app.jinja_env.globals['timezone'] = timezone


bcrypt=Bcrypt(app)
login_manager=LoginManager()
migrate=Migrate(app,db)
login_manager.login_view='login'
login_manager.init_app(app)
db.init_app(app)

load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(USER, int(user_id))
    

@app.template_filter('format_date')
def format_data(value,format='%a %H:%M'):
    if not value:
        return ''
    return value.strftime(format)

@app.route('/')
def page():
    return render_template('login.html')

@app.route('/create_post', methods=['GET'])
@login_required
def create_post():
    return render_template('post.html')


@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.now(timezone.utc)
        db.session.commit()

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        full_name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')

        if not all([full_name,email,password]):
            flash('Invalid data provided!')
        else:
            user=USER.query.filter_by(email=email).first()
            if user:
                flash('Email is already taken. Please choose another one!')
    
            else:
                hashed_password=generate_password_hash(password)
        
                new_user=USER(full_name=full_name,email=email,password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
        
                flash('You registered successfully! Now you can log in')
                return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login',methods=['GET','POST'])
def login(): 
    comments=COMMENT.query.all()
    posts=POST.query.all()
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        current_utc = datetime.now(timezone.utc)
       

        if not all([email,password]):
            flash('Invalid data provided!')

        else:
            user=USER.query.filter_by(email=email).first() 
            if not user:
                flash('Username was not found. Please register first')
                return redirect(url_for('register'))
            elif check_password_hash(user.password,password):
                session['user_id']=user.id
                login_user(user)
                flash('You logged in succeessfully!')
                return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
            else:
                flash('Invalid username or password')
    
    return render_template('login.html')




@app.route('/post',methods=['GET','POST'])
@login_required
def post(): 
    from config import UPLOAD_FOLDER
    if request.method=='POST':
        user_id=current_user.id
        post=request.form.get('post')
        image=request.files.get('image')
        images=None
        
        if not post and not image:
            flash('Both fields cannot be empty!')
            return redirect(url_for('post'))
        else:
            if image:
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)
                    images=filename
                else:
                    flash('Invalid file format')
                    return redirect(url_for('post'))

            new_post=POST(user_id=user_id,post=post,images=images)
    
            db.session.add(new_post)
            db.session.commit()
    posts=POST.query.all()
    comments=COMMENT.query.all()
    current_utc = datetime.now(timezone.utc)
    user_id=session['user_id']
    return render_template('page.html',posts=posts,comments=comments,current_utc=current_utc)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/post/<int:post_id>/like', methods=['GET','POST'])
@login_required
def post_like(post_id):
    if request.method=='POST':
        user_id = current_user.id
        existing_like = LIKE.query.filter_by(user_id=user_id, post_id=post_id).first()

        if existing_like:
            flash('You have already liked this post.')
        else:
            like = LIKE(user_id=user_id, post_id=post_id)
            db.session.add(like)
            db.session.commit()
            flash('Post liked successfully!', 'success')
        
    comments=COMMENT.query.all()
    posts=POST.query.all()
    current_utc = datetime.now(timezone.utc)
    return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)

@app.route('/post/<int:post_id>/unlike', methods=['GET','POST'])
@login_required
def post_unlike(post_id):
    post = POST.query.get_or_404(post_id)
    current_utc = datetime.now(timezone.utc)
    
    like = LIKE.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    
    if like is None:
        flash('You cannot unlike this post.')
        likes = LIKE.query.filter_by(post_id=post_id).all()
        return render_template('post_likes.html', post=post, likes=likes, current_utc=current_utc)
    
    else:
        db.session.delete(like)
        db.session.commit()
        flash('Post unliked successfully!')
    
    likes = LIKE.query.filter_by(post_id=post_id).all()
    return render_template('post_likes.html', post=post, likes=likes, current_utc=current_utc)
    


@app.route('/post/<int:post_id>/likes')
@login_required
def post_likes(post_id):
    post = POST.query.get_or_404(post_id)
    likes = LIKE.query.filter_by(post_id=post_id).all()
    current_utc = datetime.now(timezone.utc)
    return render_template('post_likes.html', post=post, likes=likes,current_utc=current_utc)

@app.route('/comments/<int:post_id>')
@login_required
def comments(post_id):
    post = POST.query.get_or_404(post_id)
    comments = COMMENT.query.filter_by(post_id=post_id).all()
    current_utc = datetime.now(timezone.utc)
    return render_template('comment.html', post=post, comments=comments,current_utc=current_utc)



@app.route('/comment',methods=['GET','POST'])
@login_required
def comment():
    comments=COMMENT.query.all()
    posts=POST.query.all()
    current_utc = datetime.now(timezone.utc)
    if request.method=='POST':
        user_id=current_user.id
        post_id=request.form.get('post_id')
        comment=request.form.get('comment')
        if not post_id :
            flash('Post ID is missing.')
            return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
        
        elif not comment:
            flash('Comment is empty.' )
            return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
        
        else:
            new_comment=COMMENT(user_id=user_id,comment=comment,post_id=post_id,answer=False,recipient=0)
    
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully!')
    
    return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)



@app.route('/reply',methods=['GET','POST'])
@login_required
def reply():
    comments=COMMENT.query.all()
    current_utc = datetime.now(timezone.utc)
    if request.method=='POST':
        user_id=current_user.id
        post_id=request.form.get('post_id')
        comment_id = request.form.get('comment_id')  
        reply=request.form.get('reply')

        comment = COMMENT.query.get(comment_id)

        if not comment:
            flash('Comment not found!')
            return render_template('comment.html',post=post_id, comments=comments,current_utc=current_utc)
        
        elif not reply:
            flash('Reply is empty.')
            return render_template('comment.html',post=post_id, comments=comments,current_utc=current_utc)
        else:
            recipient_id = comment.user_id
            new_comment=COMMENT(user_id=user_id,comment=reply,post_id=post_id,answer=True,recipient=recipient_id)
    
            db.session.add(new_comment)
            db.session.commit()
            flash('Reply added successfully!')
    
    return render_template('comment.html',post=post_id, comments=comments,current_utc=current_utc)

@app.route('/delete_comment', methods=['GET','POST'])
@login_required
def delete_comment():
    comments=COMMENT.query.all()
    posts=POST.query.all() 
    current_utc = datetime.now(timezone.utc)
    if request.method == 'POST':
        comment_id = request.form.get('comment_id')
        post_id = request.form.get('post_id')
        if not comment_id and post_id:
            flash('There is no comment to delete')
            return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
        else:
            comment = COMMENT.query.filter_by(id=comment_id,post_id=post_id).first()
    
            if not comment:
                flash('Comment not found.')
                return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
            
            elif comment.user_id != current_user.id:
                flash('You do not have permission to delete this comment.')
            else:
                db.session.delete(comment)
                db.session.commit()
                flash('Comment deleted successfully!')
    posts = POST.query.options(joinedload(POST.user)).all()
    return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)

@app.route('/delete_post', methods=['GET','POST'])
@login_required
def delete_post():
    comments=COMMENT.query.all()
    posts=POST.query.all() 
    current_utc = datetime.now(timezone.utc)
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        
        if not post_id:
            flash('There is no post to delete')
            return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
        else:
            post = POST.query.filter_by(id=post_id).first()
    
            if not post:
                flash('Post not found!')
                return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)
            
            elif post.user_id != current_user.id:
                flash('You do not have permission to delete this post!')
            else:
                LIKE.query.filter_by(post_id=post_id).delete()
                COMMENT.query.filter_by(post_id=post_id).delete()
                db.session.delete(post)
                db.session.commit()
                flash('Post deleted successfully!')
    posts = POST.query.options(joinedload(POST.user)).all()
    return render_template('page.html',comments=comments,posts=posts,current_utc=current_utc)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You logged out successfully!')
    return redirect(url_for('login'))

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        db.session.close()
    app.run()




