// SmartStay Hotel Management System - Custom JavaScript

// Document Ready Function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize date validators
    initializeDateValidators();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize auto-refresh for dashboards
    initializeAutoRefresh();
});

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Date Validation Functions
function initializeDateValidators() {
    const checkInDate = document.getElementById('check_in_date');
    const checkOutDate = document.getElementById('check_out_date');
    
    if (checkInDate && checkOutDate) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        checkInDate.setAttribute('min', today);
        checkOutDate.setAttribute('min', today);
        
        // Update check-out date minimum when check-in date changes
        checkInDate.addEventListener('change', function() {
            const checkIn = new Date(this.value);
            const minCheckOut = new Date(checkIn);
            minCheckOut.setDate(minCheckOut.getDate() + 1);
            checkOutDate.setAttribute('min', minCheckOut.toISOString().split('T')[0]);
            
            // Clear check-out date if it's before the new minimum
            if (checkOutDate.value && new Date(checkOutDate.value) <= checkIn) {
                checkOutDate.value = '';
            }
        });
        
        // Calculate total amount when dates are selected
        checkOutDate.addEventListener('change', calculateTotalAmount);
    }
}

// Calculate Total Amount for Bookings
function calculateTotalAmount() {
    const checkInDate = document.getElementById('check_in_date');
    const checkOutDate = document.getElementById('check_out_date');
    const pricePerNight = parseFloat(document.getElementById('price_per_night')?.value || 0);
    
    if (checkInDate.value && checkOutDate.value && pricePerNight > 0) {
        const checkIn = new Date(checkInDate.value);
        const checkOut = new Date(checkOutDate.value);
        const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
        
        if (nights > 0) {
            const totalAmount = nights * pricePerNight;
            const totalAmountElement = document.getElementById('total_amount');
            if (totalAmountElement) {
                totalAmountElement.textContent = `$${totalAmount.toFixed(2)}`;
                totalAmountElement.style.display = 'block';
            }
        }
    }
}

// Form Validation Functions
function initializeFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    
    // Check required fields
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validate email format
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validate password strength
    const passwordFields = form.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        if (field.value && field.value.length < 6) {
            showFieldError(field, 'Password must be at least 6 characters long');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Animation Functions
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Auto-refresh for Dashboard Data
function initializeAutoRefresh() {
    const dashboardPages = ['admin_dashboard', 'receptionist_dashboard'];
    const currentPath = window.location.pathname;
    
    if (dashboardPages.some(page => currentPath.includes(page))) {
        // Refresh dashboard data every 30 seconds
        setInterval(() => {
            refreshDashboardData();
        }, 30000);
    }
}

function refreshDashboardData() {
    // Show loading indicator
    showLoadingIndicator();
    
    // Simulate data refresh (in a real application, this would be an AJAX call)
    setTimeout(() => {
        hideLoadingIndicator();
        console.log('Dashboard data refreshed');
    }, 1000);
}

// Loading Indicator Functions
function showLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-indicator';
    loadingDiv.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center';
    loadingDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
    loadingDiv.style.zIndex = '9999';
    loadingDiv.innerHTML = '<div class="loading"></div>';
    
    document.body.appendChild(loadingDiv);
}

function hideLoadingIndicator() {
    const loadingDiv = document.getElementById('loading-indicator');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Confirmation Dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function getStatusBadgeClass(status) {
    const statusClasses = {
        'confirmed': 'bg-success',
        'cancelled': 'bg-danger',
        'pending': 'bg-warning',
        'paid': 'bg-success',
        'unpaid': 'bg-warning'
    };
    
    return statusClasses[status] || 'bg-secondary';
}

// Room Availability Check
function checkRoomAvailability(roomId, checkInDate, checkOutDate) {
    // This would make an AJAX call to check room availability
    // For now, return a promise that resolves to true
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(true);
        }, 500);
    });
}

// Booking Management
function cancelBooking(bookingId) {
    confirmAction('Are you sure you want to cancel this booking?', () => {
        // This would make an AJAX call to cancel the booking
        window.location.href = `/cancel_booking/${bookingId}`;
    });
}

function processPayment(bookingId) {
    confirmAction('Process payment for this booking?', () => {
        // This would make an AJAX call to process payment
        window.location.href = `/process_payment/${bookingId}`;
    });
}

// Staff Management
function deleteStaff(userId) {
    confirmAction('Are you sure you want to delete this staff member?', () => {
        window.location.href = `/delete_staff/${userId}`;
    });
}

// Search and Filter Functions
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            filterTable(searchTerm);
        });
    }
}

function filterTable(searchTerm) {
    const tableRows = document.querySelectorAll('tbody tr');
    
    tableRows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Print Functionality
function printPage() {
    window.print();
}

// Export Data Functions
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csv = [];
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        
        cols.forEach(col => {
            rowData.push(col.textContent.trim());
        });
        
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    downloadFile(csvContent, filename, 'text/csv');
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    window.URL.revokeObjectURL(url);
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl+P for print
    if (event.ctrlKey && event.key === 'p') {
        event.preventDefault();
        printPage();
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// Error Handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    showNotification('An unexpected error occurred. Please try again.', 'danger');
});

// Performance Monitoring
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`Page loaded in ${loadTime.toFixed(2)} milliseconds`);
});
