// js/auth.js

// Import the API_BASE_URL from your config file if you're using modules,
// or ensure config.js is loaded before auth.js in your HTML.
// (e.g., <script src="js/config.js"></script> <script src="js/auth.js"></script>)

async function checkAuth() {
    if (TEST_MODE) {
        document.body.classList.add('is-admin');
        return true;
    }

    try {
        // Construct the full API URL using the base URL
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


async function logout() {
    if (TEST_MODE) {
        // In test mode, we might just simulate a logout and redirect
        console.log("Simulating logout in TEST_MODE");
        window.location.href = '/login.html';
        return;
    }
    try {
        // Send a request to your server's logout endpoint
        const response = await fetch(`${API_BASE_URL}/user/logout`, {
            method: 'POST', // or GET, depending on your API
            credentials: 'include',
        });

        if (response.ok) {
            // If logout was successful on the server, redirect the user
            console.log("Logout successful");
            window.location.href = '/login.html'; // Or wherever your login page is
        } else {
            console.error('Logout failed on the server.');
        }
    } catch (error) {
        console.error('Logout failed:', error);
    }
}