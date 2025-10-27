// Register functionality
document.addEventListener('DOMContentLoaded', () => {
    // Redirect if already authenticated
    if (isAuthenticated()) {
        window.location.href = './companies.html';
        return;
    }
    
    const registerForm = document.getElementById('registerForm');
    
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirm_password = document.getElementById('confirm_password').value;
        
        // Validate passwords match
        if (password !== confirm_password) {
            showAlert('Las contraseñas no coinciden');
            return;
        }
        
        // Validate password length
        if (password.length < 6) {
            showAlert('La contraseña debe tener al menos 6 caracteres');
            return;
        }
        
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Registrando...';
        
        try {
            const data = await apiRequest('/auth/register', {
                method: 'POST',
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            });
            
            // Save token and user data
            setToken(data.token);
            setUserData(data.user);
            
            showAlert('¡Registro exitoso! Redirigiendo...', 'success');
            
            // Redirect to companies page
            setTimeout(() => {
                window.location.href = './companies.html';
            }, 1500);
            
        } catch (error) {
            showAlert(error.message);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Registrarse';
        }
    });
});
