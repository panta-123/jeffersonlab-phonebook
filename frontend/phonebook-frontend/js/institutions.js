// js/institutions.js

let allInstitutions = [];
// This global variable will be set in institutions.html
// to track the admin status
let isAdmin = false;

// Load institutions from API
async function loadInstitutions() {
    try {
        const response = await fetch(`${API_BASE_URL}/institutions`, {
            credentials: 'include'
        });
        console.log('Institutions fetch status:', response.status);


        if (!response.ok) {
            throw new Error('Failed to fetch institutions');
        }

        allInstitutions = await response.json();
        // Pass the isAdmin status to the rendering function
        renderInstitutions(allInstitutions, isAdmin);
    } catch (error) {
        console.error('Error loading institutions:', error);
        alert('Failed to load institutions. Please try again.');
    }
}

// Render institutions to the table
function renderInstitutions(institutions, isAdmin) {
    const tableBody = document.getElementById('institutionsTableBody');
    tableBody.innerHTML = '';

    // --- Layer 2: Conditional UI Rendering ---
    // Hide or show the "Actions" header based on admin status
    const actionsHeader = document.querySelector('th.admin-only');
    if (actionsHeader) {
        actionsHeader.style.display = isAdmin ? '' : 'none';
    }

    institutions.forEach(institution => {
        const row = document.createElement('tr');

        // Conditionally render the actions column
        const actionsCell = isAdmin ? `
            <td class="actions">
                <button class="btn-edit" data-id="${institution.id}">Edit</button>
            </td>
        ` : `
            <td class="actions"></td>
        `;

        row.innerHTML = `
            <td>${institution.id}</td>
            <td>${institution.full_name}</td>
            <td>${institution.short_name}</td>
            <td>${institution.country}</td>
            <td>${institution.city || 'N/A'}</td>
            <td>${institution.date_added}</td>
            <td>${institution.is_active ? 'Active' : 'Inactive'}</td>
            ${actionsCell}
        `;

        tableBody.appendChild(row);
    });

    // Add event listeners only if the user is an admin
    if (isAdmin) {
        document.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', () => openEditModal(btn.dataset.id));
        });
    }
}

// Search functionality
document.getElementById('searchInput').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();

    if (!searchTerm) {
        // Pass the current admin status
        renderInstitutions(allInstitutions, isAdmin);
        return;
    }

    const filtered = allInstitutions.filter(inst =>
        inst.full_name.toLowerCase().includes(searchTerm) ||
        inst.short_name.toLowerCase().includes(searchTerm) ||
        inst.country.toLowerCase().includes(searchTerm) ||
        (inst.city && inst.city.toLowerCase().includes(searchTerm))
    );

    // Pass the current admin status
    renderInstitutions(filtered, isAdmin);
});

// Export to CSV
document.getElementById('exportBtn').addEventListener('click', () => {
    const institutions = allInstitutions;
    const headers = [
        'ID',
        'Full Name',
        'Short Name',
        'Country',
        'Region',
        'City',
        'Address',
        'Date Added',
        'Date Removed',
        'Active'
    ];

    let csvContent = headers.join(',') + '\n';

    institutions.forEach(inst => {
        const row = [
            inst.id,
            `"${inst.full_name}"`,
            `"${inst.short_name}"`,
            inst.country,
            inst.region || '',
            inst.city || '',
            `"${inst.address || ''}"`,
            inst.date_added,
            inst.date_removed || '',
            inst.is_active ? 'Yes' : 'No'
        ];
        csvContent += row.join(',') + '\n';
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'institutions.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// Edit modal functions
const modal = document.getElementById('editModal');
const closeBtn = document.querySelector('.close');

function openEditModal(institutionId) {
    // You could also add an isAdmin check here for a better user experience
    // but the form submission check is the most critical part.
    const institution = allInstitutions.find(i => i.id == institutionId);
    if (!institution) return;

    document.getElementById('editInstitutionId').value = institution.id;
    document.getElementById('editFullName').value = institution.full_name;
    document.getElementById('editShortName').value = institution.short_name;
    document.getElementById('editCountry').value = institution.country;
    document.getElementById('editRegion').value = institution.region || '';
    document.getElementById('editCity').value = institution.city || '';
    document.getElementById('editAddress').value = institution.address || '';
    document.getElementById('editStatus').value = institution.is_active;

    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Handle form submission
document.getElementById('editInstitutionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // --- Layer 3: Client-Side Request Validation ---
    // This is a critical check to prevent unauthorized requests from even being sent.
    if (!isAdmin) {
        console.error('Permission denied: Not an administrator.');
        alert('You do not have permission to edit institutions.');
        return;
    }

    const institutionId = document.getElementById('editInstitutionId').value;
    const institutionData = {
        full_name: document.getElementById('editFullName').value,
        short_name: document.getElementById('editShortName').value,
        country: document.getElementById('editCountry').value,
        region: document.getElementById('editRegion').value || null,
        city: document.getElementById('editCity').value || null,
        address: document.getElementById('editAddress').value || null,
        is_active: document.getElementById('editStatus').value === 'true'
    };

    try {
        const response = await fetch(`${API_BASE_URL}/institutions/${institutionId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(institutionData),
            credentials: 'include'
        });

        if (!response.ok) {
            // A 403 Forbidden status would be an example of a backend check failing
            if (response.status === 403) {
                throw new Error('Permission denied.');
            }
            throw new Error('Failed to update institution');
        }

        await loadInstitutions();
        closeModal();
    } catch (error) {
        console.error('Error updating institution:', error);
        alert('Failed to update institution. Please try again.');
    }
});