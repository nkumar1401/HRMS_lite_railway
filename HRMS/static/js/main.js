/**
 * HRMS Lite - Main JavaScript
 * Handles form validation, AJAX operations, modals, and dynamic interactions
 */

// ============================================
// Global State & Configuration
// ============================================
let deleteItemId = null;
let deleteItemUrl = null;

// ============================================
// DOM Ready
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeSearch();
    initializeModals();
    initializeFormValidation();
});

// ============================================
// Sidebar Toggle (Mobile)
// ============================================
function initializeSidebar() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
        
        // Close sidebar when clicking outside
        document.addEventListener('click', function(e) {
            if (sidebar.classList.contains('active') && 
                !sidebar.contains(e.target) && 
                !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        });
    }
}

// ============================================
// Search Functionality
// ============================================
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    let searchTimeout;
    
    // Handle Enter key
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            clearTimeout(searchTimeout);
            performSearch(this.value.trim());
        }
    });
}

function performSearch(query) {
    const currentUrl = new URL(window.location.href);
    
    if (query) {
        currentUrl.searchParams.set('search', query);
    } else {
        currentUrl.searchParams.delete('search');
    }
    currentUrl.searchParams.delete('page');
    
    window.location.href = currentUrl.toString();
}

// ============================================
// Delete Modal
// ============================================
function initializeModals() {
    const modal = document.getElementById('deleteModal');
    if (!modal) return;
    
    // Close modal on backdrop click
    const backdrop = modal.querySelector('.modal-backdrop');
    if (backdrop) {
        backdrop.addEventListener('click', closeModal);
    }
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

function showDeleteModal(id, name) {
    const modal = document.getElementById('deleteModal');
    const itemNameEl = document.getElementById('deleteItemName');
    
    if (!modal) return;
    
    deleteItemId = id;
    
    // Try to get the delete URL from the page's script
    if (typeof getDeleteUrl === 'function') {
        deleteItemUrl = getDeleteUrl(id);
    }
    
    if (itemNameEl) {
        itemNameEl.textContent = name;
    }
    
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    deleteItemId = null;
    deleteItemUrl = null;
}

function confirmDelete() {
    if (!deleteItemId || !deleteItemUrl) {
        console.error('Delete URL not set');
        return;
    }
    
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = 'Deleting...';
    }
    
    // Get CSRF token
    const csrfToken = getCSRFToken();
    
    fetch(deleteItemUrl, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Delete failed');
        }
        return response.json();
    })
    .then(data => {
        closeModal();
        
        if (data.success) {
            showToast(data.message || 'Deleted successfully!', 'success');
            
            // Remove the row from the table
            const row = document.querySelector(`tr[data-id="${deleteItemId}"]`);
            if (row) {
                row.style.transition = 'opacity 0.3s, transform 0.3s';
                row.style.opacity = '0';
                row.style.transform = 'translateX(-20px)';
                setTimeout(() => {
                    row.remove();
                    checkEmptyTable();
                }, 300);
            } else {
                // Reload the page if we can't find the row
                setTimeout(() => location.reload(), 500);
            }
        } else {
            showToast(data.message || 'Delete failed!', 'error');
        }
    })
    .catch(error => {
        closeModal();
        showToast('An error occurred. Please try again.', 'error');
        console.error('Delete error:', error);
    })
    .finally(() => {
        if (confirmBtn) {
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = 'Delete';
        }
    });
}

function checkEmptyTable() {
    const tbody = document.querySelector('.data-table tbody');
    if (tbody && tbody.children.length === 0) {
        // Reload to show empty state
        location.reload();
    }
}

// ============================================
// Form Validation
// ============================================
function initializeFormValidation() {
    const forms = document.querySelectorAll('form.form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('.form-input, .form-select');
        
        inputs.forEach(input => {
            // Clear error on input
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
            
            // Validate on blur
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldId = field.id;
    
    // Email validation
    if (fieldId === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('input-error');
    
    const errorEl = document.getElementById(field.id + '_error');
    if (errorEl) {
        errorEl.textContent = message;
    }
}

function clearFieldError(field) {
    field.classList.remove('input-error');
    
    const errorEl = document.getElementById(field.id + '_error');
    if (errorEl) {
        errorEl.textContent = '';
    }
}

// ============================================
// Toast Notifications
// ============================================
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconSvg = type === 'success' 
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
    
    toast.innerHTML = `
        <span class="toast-icon">${iconSvg}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'toastSlide 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

// ============================================
// Utility Functions
// ============================================
function getCSRFToken() {
    // Try to get from cookie
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    
    if (cookieValue) return cookieValue;
    
    // Try to get from hidden input
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) return csrfInput.value;
    
    return '';
}

// AJAX form submission helper
function submitFormAjax(form, onSuccess, onError) {
    const formData = new FormData(form);
    const csrfToken = getCSRFToken();
    
    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (onSuccess) onSuccess(data);
        } else {
            if (onError) onError(data);
        }
    })
    .catch(error => {
        console.error('Form submission error:', error);
        if (onError) onError({ message: 'An error occurred' });
    });
}

// Debounce helper
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

// Format date helper
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}
