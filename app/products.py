from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Product
from app import db
from werkzeug.utils import secure_filename
import os

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def index():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(is_blocked=False).order_by(Product.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('products/index.html', products=products)

@products_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        
        # Handle image upload
        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('app/static/uploads', filename))
            image_url = f'/static/uploads/{filename}'
        else:
            image_url = None
        
        product = Product(
            title=title,
            description=description,
            price=price,
            category=category,
            image_url=image_url,
            seller_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!')
        return redirect(url_for('products.index'))
    
    return render_template('products/new.html')

@products_bp.route('/products/<int:id>')
def show(id):
    product = Product.query.get_or_404(id)
    if product.is_blocked:
        flash('This product has been blocked')
        return redirect(url_for('products.index'))
    return render_template('products/show.html', product=product)

@products_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id and not current_user.is_admin:
        flash('You are not authorized to edit this product')
        return redirect(url_for('products.show', id=id))
    
    if request.method == 'POST':
        product.title = request.form.get('title')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        
        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('app/static/uploads', filename))
            product.image_url = f'/static/uploads/{filename}'
        
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('products.show', id=id))
    
    return render_template('products/edit.html', product=product)

@products_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id and not current_user.is_admin:
        flash('You are not authorized to delete this product')
        return redirect(url_for('products.show', id=id))
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('products.index'))

@products_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    products = Product.query.filter_by(is_blocked=False)
    
    if query:
        products = products.filter(Product.title.ilike(f'%{query}%') | Product.description.ilike(f'%{query}%'))
    if category:
        products = products.filter_by(category=category)
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)
    
    products = products.order_by(Product.created_at.desc()).all()
    return render_template('products/search.html', products=products, query=query) 