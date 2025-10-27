// Login functionality
document.addEventListener('DOMContentLoaded', () => {
    // Redirect if already authenticated
    if (isAuthenticated()) {
        window.location.href = './companies.html';
        return;
    }
    
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const username_or_email = document.getElementById('username_or_email').value;
        const password = document.getElementById('password').value;
        
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Iniciando sesión...';
        
        try {
            const data = await apiRequest('/auth/login', {
                method: 'POST',
                body: JSON.stringify({
                    username_or_email,
                    password
                })
            });
            
            // Save token and user data
            setToken(data.token);
            setUserData(data.user);
            
            showAlert('¡Inicio de sesión exitoso!', 'success');
            
            // Redirect to companies page
            setTimeout(() => {
                window.location.href = './companies.html';
            }, 1000);
            
        } catch (error) {
            showAlert(error.message);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Iniciar Sesión';
        }
    });
});
