from app import create_app, db
from app.models import User, Subscription
from werkzeug.security import generate_password_hash
import os

app = create_app()
app.app_context().push()

def init_db():
    db.create_all()
    
    # Create admin user
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin1234')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    
    admin = User.query.filter_by(username=admin_username).first()
    if not admin:
        admin = User(username=admin_username, 
                     email=admin_email, 
                     password_hash=generate_password_hash(admin_password),
                     is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    print("Database tables created.")

if __name__ == '__main__':
    init_db()