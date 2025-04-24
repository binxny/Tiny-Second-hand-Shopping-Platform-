from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Product, Message
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an admin to access this page')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@login_required
@admin_required
def index():
    users = User.query.all()
    products = Product.query.all()
    messages = Message.query.all()
    return render_template('admin/index.html', users=users, products=products, messages=messages)

@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/users/<int:id>/block', methods=['POST'])
@login_required
@admin_required
def block_user(id):
    user = User.query.get_or_404(id)
    user.is_blocked = True
    db.session.commit()
    flash(f'User {user.username} has been blocked')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/users/<int:id>/unblock', methods=['POST'])
@login_required
@admin_required
def unblock_user(id):
    user = User.query.get_or_404(id)
    user.is_blocked = False
    db.session.commit()
    flash(f'User {user.username} has been unblocked')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/admin/products/<int:id>/block', methods=['POST'])
@login_required
@admin_required
def block_product(id):
    product = Product.query.get_or_404(id)
    product.is_blocked = True
    db.session.commit()
    flash(f'Product {product.title} has been blocked')
    return redirect(url_for('admin.products'))

@admin_bp.route('/admin/products/<int:id>/unblock', methods=['POST'])
@login_required
@admin_required
def unblock_product(id):
    product = Product.query.get_or_404(id)
    product.is_blocked = False
    db.session.commit()
    flash(f'Product {product.title} has been unblocked')
    return redirect(url_for('admin.products'))

@admin_bp.route('/admin/messages')
@login_required
@admin_required
def messages():
    messages = Message.query.all()
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/admin/messages/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully')
    return redirect(url_for('admin.messages')) 