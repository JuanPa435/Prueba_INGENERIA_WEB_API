// Dashboard functionality
let currentCompany = null;

document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    
    // Get selected company
    currentCompany = getSelectedCompany();
    
    if (!currentCompany) {
        window.location.href = './companies.html';
        return;
    }
    
    // Update page title
    document.getElementById('companyName').textContent = `📦 ${currentCompany.name}`;
    
    // Show admin panel if user is admin
    if (currentCompany.role === 'admin') {
        document.getElementById('adminPanel').classList.remove('hidden');
    }
    
    // Load products
    loadProducts();
    
    // Product form submit
    document.getElementById('productForm').addEventListener('submit', handleProductSubmit);
});

async function loadProducts() {
    const productsList = document.getElementById('productsList');
    productsList.innerHTML = '<div class="loading">Cargando productos...</div>';
    
    try {
        const data = await apiRequest(`/companies/${currentCompany.id}/productos`);
        
        if (!data || data.length === 0) {
            productsList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📦</div>
                    <p>No hay productos registrados aún.</p>
                </div>
            `;
            return;
        }
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Precio</th>
                        <th>Cantidad</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.forEach(product => {
            html += `
                <tr>
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>$${parseFloat(product.price).toFixed(2)}</td>
                    <td>${product.quantity}</td>
                    <td>
                        <button onclick="editProduct(${product.id})" class="btn btn-secondary" style="margin-right: 5px;">✏️</button>
                        ${currentCompany.role === 'admin' ? 
                            `<button onclick="deleteProduct(${product.id})" class="btn btn-danger">🗑️</button>` : 
                            ''
                        }
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        productsList.innerHTML = html;
        
    } catch (error) {
        productsList.innerHTML = `<div class="alert alert-error">${error.message}</div>`;
    }
}

function openAddProductModal() {
    document.getElementById('modalTitle').textContent = 'Agregar Producto';
    document.getElementById('productForm').reset();
    document.getElementById('product_id').value = '';
    document.getElementById('productModal').style.display = 'block';
}

function closeProductModal() {
    document.getElementById('productModal').style.display = 'none';
}

async function editProduct(id) {
    try {
        const product = await apiRequest(`/companies/${currentCompany.id}/productos/${id}`);
        
        document.getElementById('modalTitle').textContent = 'Editar Producto';
        document.getElementById('product_id').value = product.id;
        document.getElementById('product_name').value = product.name;
        document.getElementById('product_description').value = product.description;
        document.getElementById('product_price').value = product.price;
        document.getElementById('product_quantity').value = product.quantity;
        
        document.getElementById('productModal').style.display = 'block';
        
    } catch (error) {
        showAlert(error.message);
    }
}

async function handleProductSubmit(e) {
    e.preventDefault();
    hideAlert();
    
    const productId = document.getElementById('product_id').value;
    const productData = {
        name: document.getElementById('product_name').value,
        description: document.getElementById('product_description').value,
        price: parseFloat(document.getElementById('product_price').value),
        quantity: parseInt(document.getElementById('product_quantity').value)
    };
    
    try {
        if (productId) {
            // Update existing product
            await apiRequest(`/companies/${currentCompany.id}/productos/${productId}`, {
                method: 'PUT',
                body: JSON.stringify(productData)
            });
            showAlert('Producto actualizado exitosamente!', 'success');
        } else {
            // Create new product
            await apiRequest(`/companies/${currentCompany.id}/productos`, {
                method: 'POST',
                body: JSON.stringify(productData)
            });
            showAlert('Producto creado exitosamente!', 'success');
        }
        
        closeProductModal();
        loadProducts();
        
    } catch (error) {
        showAlert(error.message);
    }
}

async function deleteProduct(id) {
    if (!confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        return;
    }
    
    try {
        await apiRequest(`/companies/${currentCompany.id}/productos/${id}`, {
            method: 'DELETE'
        });
        
        showAlert('Producto eliminado exitosamente!', 'success');
        loadProducts();
        
    } catch (error) {
        showAlert(error.message);
    }
}

// Employees functions
async function showEmployees() {
    document.getElementById('employeesModal').style.display = 'block';
    const employeesList = document.getElementById('employeesList');
    employeesList.innerHTML = '<div class="loading">Cargando empleados...</div>';
    
    try {
        const data = await apiRequest(`/companies/${currentCompany.id}/employees`);
        
        if (!data.employees || data.employees.length === 0) {
            employeesList.innerHTML = '<p>No hay empleados registrados.</p>';
            return;
        }
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Usuario</th>
                        <th>Email</th>
                        <th>Rol</th>
                        <th>Fecha de Ingreso</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.employees.forEach(employee => {
            const joinDate = new Date(employee.joined_at).toLocaleDateString();
            html += `
                <tr>
                    <td>${employee.id}</td>
                    <td>${employee.username}</td>
                    <td>${employee.email}</td>
                    <td>
                        <span style="color: ${employee.role === 'admin' ? 'var(--danger-color)' : 'var(--secondary-color)'}">
                            ${employee.role === 'admin' ? '👑 Admin' : '👤 Empleado'}
                        </span>
                    </td>
                    <td>${joinDate}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        employeesList.innerHTML = html;
        
    } catch (error) {
        employeesList.innerHTML = `<div class="alert alert-error">${error.message}</div>`;
    }
}

function closeEmployeesModal() {
    document.getElementById('employeesModal').style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    const productModal = document.getElementById('productModal');
    const employeesModal = document.getElementById('employeesModal');
    
    if (event.target === productModal) {
        closeProductModal();
    }
    if (event.target === employeesModal) {
        closeEmployeesModal();
    }
}
