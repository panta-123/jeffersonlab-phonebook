let allMembers = [];

// Load members from API
async function loadMembers() {
    try {
        const response = await fetch(`${API_BASE_URL}/members`, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to fetch members');
        }

        allMembers = await response.json();
        renderMembers(allMembers);
    } catch (error) {
        console.error('Error loading members:', error);
        alert('Failed to load members. Please try again.');
    }
}

// Render members to the table
function renderMembers(members) {
    const tableBody = document.getElementById('membersTableBody');
    tableBody.innerHTML = '';

    members.forEach(member => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${member.id}</td>
            <td>${member.first_name}</td>
            <td>${member.last_name}</td>
            <td>${member.email}</td>
            <td>${member.institution?.full_name || 'N/A'}</td>
            <td>${member.date_joined}</td>
            <td>${member.is_active ? 'Active' : 'Inactive'}</td>
            <td class="admin-only">
                <button class="btn-edit" data-id="${member.id}">Edit</button>
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
        renderMembers(allMembers);
        return;
    }

    const filtered = allMembers.filter(member =>
        member.first_name.toLowerCase().includes(searchTerm) ||
        member.last_name.toLowerCase().includes(searchTerm) ||
        member.email.toLowerCase().includes(searchTerm) ||
        (member.institution?.full_name && member.institution.full_name.toLowerCase().includes(searchTerm))
    );

    renderMembers(filtered);
});

// Export to CSV
document.getElementById('exportBtn').addEventListener('click', () => {
    const members = allMembers;
    const headers = [
        'ID',
        'First Name',
        'Last Name',
        'Email',
        'ORCID',
        'Preferred Author Name',
        'Institution',
        'Date Joined',
        'Date Left',
        'Active'
    ];

    let csvContent = headers.join(',') + '\n';

    members.forEach(member => {
        const row = [
            member.id,
            `"${member.first_name}"`,
            `"${member.last_name}"`,
            member.email,
            member.orcid || '',
            member.preferred_author_name || '',
            `"${member.institution?.full_name || ''}"`,
            member.date_joined,
            member.date_left || '',
            member.is_active ? 'Yes' : 'No'
        ];
        csvContent += row.join(',') + '\n';
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'members.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// Edit modal functions
const modal = document.getElementById('editModal');
const closeBtn = document.querySelector('.close');

function openEditModal(memberId) {
    const member = allMembers.find(m => m.id == memberId);
    if (!member) return;

    document.getElementById('editMemberId').value = member.id;
    document.getElementById('editFirstName').value = member.first_name;
    document.getElementById('editLastName').value = member.last_name;
    document.getElementById('editEmail').value = member.email;
    document.getElementById('editStatus').value = member.is_active;

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
document.getElementById('editMemberForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const memberId = document.getElementById('editMemberId').value;
    const memberData = {
        first_name: document.getElementById('editFirstName').value,
        last_name: document.getElementById('editLastName').value,
        email: document.getElementById('editEmail').value,
        is_active: document.getElementById('editStatus').value === 'true'
    };

    try {
        const response = await fetch(`/api/members/${memberId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(memberData),
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to update member');
        }

        // Refresh the members list
        await loadMembers();
        closeModal();
    } catch (error) {
        console.error('Error updating member:', error);
        alert('Failed to update member. Please try again.');
    }
});