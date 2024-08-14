from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User, Subscription
from app import db
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        
        subscription_plan = request.form['subscription_plan']
        if user.subscription:
            user.subscription.plan = subscription_plan
            user.subscription.end_date = datetime.utcnow() + timedelta(days=30)
        else:
            new_subscription = Subscription(plan=subscription_plan, 
                                            end_date=datetime.utcnow() + timedelta(days=30))
            user.subscription = new_subscription
        
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('edit_user.html', user=user)

@bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot delete admin user.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    
    return redirect(url_for('admin.admin_dashboard'))