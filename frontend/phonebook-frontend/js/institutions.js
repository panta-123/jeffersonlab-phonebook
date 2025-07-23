let allInstitutions = [];

// Load institutions from API
async function loadInstitutions() {
    try {
        const response = await fetch(`${API_BASE_URL}/institutions`, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to fetch institutions');
        }

        allInstitutions = await response.json();
        renderInstitutions(allInstitutions);
    } catch (error) {
        console.error('Error loading institutions:', error);
        alert('Failed to load institutions. Please try again.');
    }
}

// Render institutions to the table
function renderInstitutions(institutions) {
    const tableBody = document.getElementById('institutionsTableBody');
    tableBody.innerHTML = '';

    institutions.forEach(institution => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${institution.id}</td>
            <td>${institution.full_name}</td>
            <td>${institution.short_name}</td>
            <td>${institution.country}</td>
            <td>${institution.city || 'N/A'}</td>
            <td>${institution.date_added}</td>
            <td>${institution.is_active ? 'Active' : 'Inactive'}</td>
            <td class="admin-only">
                <button class="btn-edit" data-id="${institution.id}">Edit</button>
            </td>
        `;

        tableBody.appendChild(row);
    });

    // Add event listeners to edit buttons
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', () => openEditModal(btn.dataset.id));
    });
}

// Search functionality
document.getElementById('searchInput').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();

    if (!searchTerm) {
        renderInstitutions(allInstitutions);
        return;
    }

    const filtered = allInstitutions.filter(inst =>
        inst.full_name.toLowerCase().includes(searchTerm) ||
        inst.short_name.toLowerCase().includes(searchTerm) ||
        inst.country.toLowerCase().includes(searchTerm) ||
        (inst.city && inst.city.toLowerCase().includes(searchTerm))
    );

    renderInstitutions(filtered);
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
        const response = await fetch(`${API_BASE_URL}/${institutionId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(institutionData),
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to update institution');
        }

        // Refresh the institutions list
        await loadInstitutions();
        closeModal();
    } catch (error) {
        console.error('Error updating institution:', error);
        alert('Failed to update institution. Please try again.');
    }
});