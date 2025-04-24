from flask import Blueprint, render_template
from app.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_products = Product.query.filter_by(is_blocked=False).order_by(Product.created_at.desc()).limit(8).all()
    return render_template('main/index.html', featured_products=featured_products)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html') 