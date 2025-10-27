// Companies functionality
document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    
    loadCompanies();
    
    // Create company form
    document.getElementById('createCompanyForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const name = document.getElementById('company_name').value;
        const description = document.getElementById('company_description').value;
        
        try {
            const data = await apiRequest('/companies', {
                method: 'POST',
                body: JSON.stringify({ name, description })
            });
            
            showAlert(`Empresa creada exitosamente! Código único: ${data.unique_code}`, 'success');
            
            // Clear form
            document.getElementById('createCompanyForm').reset();
            
            // Reload companies
            loadCompanies();
            
        } catch (error) {
            showAlert(error.message);
        }
    });
    
    // Join company form
    document.getElementById('joinCompanyForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();
        
        const unique_code = document.getElementById('unique_code').value.trim().toUpperCase();
        
        try {
            await apiRequest('/companies/join', {
                method: 'POST',
                body: JSON.stringify({ unique_code })
            });
            
            showAlert('Te has unido a la empresa exitosamente!', 'success');
            
            // Clear form
            document.getElementById('joinCompanyForm').reset();
            
            // Reload companies
            loadCompanies();
            
        } catch (error) {
            showAlert(error.message);
        }
    });
});

async function loadCompanies() {
    const companiesList = document.getElementById('companiesList');
    companiesList.innerHTML = '<div class="loading">Cargando empresas...</div>';
    
    try {
        const data = await apiRequest('/companies');
        
        if (!data.companies || data.companies.length === 0) {
            companiesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🏢</div>
                    <p>No perteneces a ninguna empresa aún.</p>
                    <p>Crea una nueva o únete a una existente usando el código único.</p>
                </div>
            `;
            return;
        }
        
        let html = '<div class="feature-grid">';
        
        data.companies.forEach(company => {
            html += `
                <div class="feature-card" style="cursor: pointer;" onclick="selectCompany(${company.id}, '${company.name}', '${company.role}')">
                    <div class="feature-icon">🏢</div>
                    <h3>${company.name}</h3>
                    ${company.description ? `<p>${company.description}</p>` : ''}
                    <p style="margin-top: 10px;"><strong>Código:</strong> ${company.unique_code}</p>
                    <p style="margin-top: 5px;"><strong>Rol:</strong> 
                        <span style="color: ${company.role === 'admin' ? 'var(--danger-color)' : 'var(--secondary-color)'}">
                            ${company.role === 'admin' ? '👑 Admin' : '👤 Empleado'}
                        </span>
                    </p>
                    <button class="btn btn-primary" style="margin-top: 15px; width: 100%;">
                        Ver Dashboard
                    </button>
                </div>
            `;
        });
        
        html += '</div>';
        companiesList.innerHTML = html;
        
    } catch (error) {
        companiesList.innerHTML = `<div class="alert alert-error">${error.message}</div>`;
    }
}

function selectCompany(id, name, role) {
    setSelectedCompany({ id, name, role });
    window.location.href = '/pages/dashboard.html';
}
