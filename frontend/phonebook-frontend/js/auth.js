// Remove the import and use the global variable
const TEST_MODE = true;

async function checkAuth() {
    if (TEST_MODE) {
        document.body.classList.add('is-admin');
        return true;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/user/check-auth`, {
            credentials: 'include'
        });

        if (!response.ok) return true;

        const data = await response.json();
        if (data.isAdmin) document.body.classList.add('is-admin');
        return data.authenticated;
    } catch (error) {
        console.error('Auth check failed:', error);
        return false;
    }
}

// ... rest of your auth.js functions