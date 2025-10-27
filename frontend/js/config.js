// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// Storage keys
const TOKEN_KEY = 'jwt_token';
const USER_KEY = 'user_data';
const COMPANY_KEY = 'selected_company';

// Get token from localStorage
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

// Set token in localStorage
function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

// Remove token from localStorage
function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
}

// Get user data from localStorage
function getUserData() {
    const data = localStorage.getItem(USER_KEY);
    return data ? JSON.parse(data) : null;
}

// Set user data in localStorage
function setUserData(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

// Remove user data from localStorage
function removeUserData() {
    localStorage.removeItem(USER_KEY);
}

// Get selected company from localStorage
function getSelectedCompany() {
    const data = localStorage.getItem(COMPANY_KEY);
    return data ? JSON.parse(data) : null;
}

// Set selected company in localStorage
function setSelectedCompany(company) {
    localStorage.setItem(COMPANY_KEY, JSON.stringify(company));
}

// Remove selected company from localStorage
function removeSelectedCompany() {
    localStorage.removeItem(COMPANY_KEY);
}

// Check if user is authenticated
function isAuthenticated() {
    return !!getToken();
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/pages/login.html';
        return false;
    }
    return true;
}

// Logout function
function logout() {
    removeToken();
    removeUserData();
    removeSelectedCompany();
    window.location.href = '/pages/login.html';
}

// Show profile
function showProfile() {
    // For now, just show an alert with user info
    const user = getUserData();
    if (user) {
        alert(`Usuario: ${user.username}\nEmail: ${user.email}`);
    }
}

// Make authenticated API request
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // If 401, token might be expired
            if (response.status === 401) {
                logout();
                throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
            }
            throw new Error(data.error || 'Error en la solicitud');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Show alert message
function showAlert(message, type = 'error') {
    const alertDiv = document.getElementById('alert');
    if (!alertDiv) return;
    
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertDiv.classList.add('hidden');
    }, 5000);
}

// Hide alert
function hideAlert() {
    const alertDiv = document.getElementById('alert');
    if (alertDiv) {
        alertDiv.classList.add('hidden');
    }
}
