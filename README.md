# Marketplace - 중고거래 플랫폼

A secure and user-friendly marketplace platform for buying and selling products.

## Features

- User Authentication
  - Registration and login system
  - User profiles
  - Password reset functionality

- Product Management
  - Create, read, update, and delete products
  - Image upload for products
  - Product categories
  - Search and filter products

- Messaging System
  - Real-time messaging between buyers and sellers
  - Message notifications
  - Message history

- Admin Panel
  - User management
  - Product moderation
  - Message monitoring
  - Platform statistics

- Security Features
  - User blocking system
  - Product blocking system
  - Secure password hashing
  - Input validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/marketplace.git
cd marketplace
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration.

5. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Configuration

The following environment variables can be set in the `.env` file:

- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection URL
- `MAIL_USERNAME`: Email username for notifications
- `MAIL_PASSWORD`: Email password for notifications

## Usage

1. Register a new account or login with existing credentials
2. Browse products or use the search functionality
3. Contact sellers through the messaging system
4. List your own products for sale
5. Manage your account and products

## Admin Access

To create an admin user:

1. Register a normal user account
2. Use the Flask shell to promote the user to admin:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='your_username').first()
    user.is_admin = True
    db.session.commit()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@marketplace.com or create an issue in the repository.
