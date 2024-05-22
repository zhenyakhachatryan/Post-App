import os 

base_dir=os.path.abspath(os.path.dirname(__file__))
db_path=os.path.join(base_dir,'user_post.db')

SQLALCHEMY_DATABASE_URI='sqlite:///'+db_path
SECRET_KEY=os.environ.get('SECRET_KEY')
UPLOAD_FOLDER='static/images'