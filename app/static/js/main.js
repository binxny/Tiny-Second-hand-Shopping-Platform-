// Socket.IO Connection
const socket = io();

// Join product room when viewing a product
if (window.location.pathname.startsWith('/products/')) {
    const productId = window.location.pathname.split('/')[2];
    socket.emit('join', { product_id: productId });
}

// Handle new messages
socket.on('new_message', function(data) {
    const messageThread = document.querySelector('.message-thread');
    if (messageThread) {
        const messageBubble = document.createElement('div');
        messageBubble.className = `message-bubble ${data.sender === currentUser ? 'sent' : 'received'}`;
        messageBubble.innerHTML = `
            <div class="message-header">
                <strong>${data.sender}</strong>
                <small>${data.timestamp}</small>
            </div>
            <div class="message-content">${data.content}</div>
        `;
        messageThread.appendChild(messageBubble);
        messageThread.scrollTop = messageThread.scrollHeight;
    }
});

// Image Preview
const imageInput = document.querySelector('input[type="file"]');
const imagePreview = document.querySelector('.image-preview');

if (imageInput && imagePreview) {
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    });
}

// Form Validation
const forms = document.querySelectorAll('.needs-validation');

Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
});

// Password Confirmation
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm_password');

if (password && confirmPassword) {
    confirmPassword.addEventListener('input', function() {
        if (this.value !== password.value) {
            this.setCustomValidity('Passwords do not match');
        } else {
            this.setCustomValidity('');
        }
    });
}

// Search Autocomplete
const searchInput = document.querySelector('input[type="search"]');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function() {
        const query = this.value;
        if (query.length >= 2) {
            fetch(`/api/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Update search results
                    const resultsContainer = document.querySelector('.search-results');
                    if (resultsContainer) {
                        resultsContainer.innerHTML = data.map(item => `
                            <a href="/products/${item.id}" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between">
                                    <h5 class="mb-1">${item.title}</h5>
                                    <small>$${item.price}</small>
                                </div>
                                <p class="mb-1">${item.description}</p>
                            </a>
                        `).join('');
                    }
                });
        }
    }, 300));
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Delete Confirmation
const deleteButtons = document.querySelectorAll('.delete-btn');
deleteButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });
});

// Message Read Status
const messageLinks = document.querySelectorAll('.message-link');
messageLinks.forEach(link => {
    link.addEventListener('click', function() {
        const messageId = this.dataset.messageId;
        fetch(`/messages/${messageId}/read`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    });
});

// Product Filter
const filterForm = document.querySelector('.filter-form');
if (filterForm) {
    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const params = new URLSearchParams(formData);
        window.location.href = `/products?${params.toString()}`;
    });
}

// Infinite Scroll
const productGrid = document.querySelector('.product-grid');
if (productGrid) {
    let page = 1;
    const loadMore = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            page++;
            fetch(`/products?page=${page}`)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newProducts = doc.querySelectorAll('.product-card');
                    newProducts.forEach(product => {
                        productGrid.appendChild(product);
                    });
                });
        }
    };
    window.addEventListener('scroll', debounce(loadMore, 200));
}

// Toast Notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Handle Flash Messages
const flashMessages = document.querySelectorAll('.alert');
flashMessages.forEach(message => {
    setTimeout(() => {
        message.classList.add('fade');
        setTimeout(() => message.remove(), 500);
    }, 5000);
}); 