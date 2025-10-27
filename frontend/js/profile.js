// Profile functionality
document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    
    loadProfile();
    
    // Update profile form
    document.getElementById('updateProfileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const new_password = document.getElementById('new_password').value;
        const confirm_password = document.getElementById('confirm_password').value;
        
        // Validate passwords match if provided
        if (new_password || confirm_password) {
            if (new_password !== confirm_password) {
                showAlert('Las contraseñas no coinciden');
                return;
            }
            
            if (new_password.length < 6) {
                showAlert('La contraseña debe tener al menos 6 caracteres');
                return;
            }
        }
        
        const updateData = {
            username,
            email
        };
        
        if (new_password) {
            updateData.password = new_password;
        }
        
        const submitBtn = document.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Actualizando...';
        
        try {
            const data = await apiRequest('/auth/profile', {
                method: 'PUT',
                body: JSON.stringify(updateData)
            });
            
            // Update stored user data
            setUserData(data.user);
            
            showAlert('Perfil actualizado exitosamente!', 'success');
            
            // Reload profile
            loadProfile();
            
            // Clear password fields
            document.getElementById('new_password').value = '';
            document.getElementById('confirm_password').value = '';
            
        } catch (error) {
            showAlert(error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Actualizar Perfil';
        }
    });
});

async function loadProfile() {
    const profileInfo = document.getElementById('profileInfo');
    profileInfo.innerHTML = '<div class="loading">Cargando perfil...</div>';
    
    try {
        const data = await apiRequest('/auth/profile');
        
        // Display profile info
        const createdDate = new Date(data.created_at).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        profileInfo.innerHTML = `
            <div style="display: grid; gap: 15px;">
                <div>
                    <strong>Usuario:</strong> ${data.username}
                </div>
                <div>
                    <strong>Email:</strong> ${data.email}
                </div>
                <div>
                    <strong>Estado:</strong> 
                    <span style="color: ${data.is_verified ? 'var(--secondary-color)' : 'var(--danger-color)'}">
                        ${data.is_verified ? '✅ Verificado' : '❌ No Verificado'}
                    </span>
                </div>
                <div>
                    <strong>Miembro desde:</strong> ${createdDate}
                </div>
            </div>
        `;
        
        // Pre-fill update form
        document.getElementById('username').value = data.username;
        document.getElementById('email').value = data.email;
        
    } catch (error) {
        profileInfo.innerHTML = `<div class="alert alert-error">${error.message}</div>`;
    }
}
