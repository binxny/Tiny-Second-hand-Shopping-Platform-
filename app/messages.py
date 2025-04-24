from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Message, Product
from app import db, socketio
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
@login_required
def index():
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) | 
        (Message.recipient_id == current_user.id)
    ).order_by(Message.timestamp.desc()).all()
    return render_template('messages/index.html', messages=messages)

@messages_bp.route('/messages/<int:product_id>/new', methods=['GET', 'POST'])
@login_required
def new(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id == current_user.id:
        flash('You cannot send a message to yourself')
        return redirect(url_for('products.show', id=product_id))
    
    if request.method == 'POST':
        content = request.form.get('content')
        message = Message(
            content=content,
            sender_id=current_user.id,
            recipient_id=product.seller_id,
            product_id=product_id
        )
        db.session.add(message)
        db.session.commit()
        
        # Emit socket event for real-time messaging
        socketio.emit('new_message', {
            'message_id': message.id,
            'content': message.content,
            'sender': current_user.username,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, room=f'product_{product_id}')
        
        flash('Message sent successfully!')
        return redirect(url_for('messages.show', id=message.id))
    
    return render_template('messages/new.html', product=product)

@messages_bp.route('/messages/<int:id>')
@login_required
def show(id):
    message = Message.query.get_or_404(id)
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('You are not authorized to view this message')
        return redirect(url_for('messages.index'))
    
    if message.recipient_id == current_user.id and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('messages/show.html', message=message)

@socketio.on('join')
def on_join(data):
    product_id = data['product_id']
    room = f'product_{product_id}'
    socketio.join_room(room)

@socketio.on('leave')
def on_leave(data):
    product_id = data['product_id']
    room = f'product_{product_id}'
    socketio.leave_room(room) 