// js/auth.js

// Import the API_BASE_URL from your config file if you're using modules,
// or ensure config.js is loaded before auth.js in your HTML.

async function checkAuth() {
    // Return a structured object with both authentication and admin status
    if (TEST_MODE) {
        document.body.classList.add('is-admin');
        return { authenticated: true, isAdmin: true };
    }

    try {
        const response = await fetch(`${API_BASE_URL}/user/check-auth`, {
            credentials: 'include'
        });

        // We must always process the JSON response
        const data = await response.json();

        // Use the data from the response body to determine status
        if (data.authenticated) {
            if (data.isAdmin) {
                document.body.classList.add('is-admin');
            }
            return { authenticated: true, isAdmin: data.isAdmin };
        } else {
            return { authenticated: false, isAdmin: false };
        }

    } catch (error) {
        // This block catches network errors or issues with JSON parsing.
        console.error('Auth check failed:', error);
        return { authenticated: false, isAdmin: false };
    }
}


async function logout() {
    if (TEST_MODE) {
        console.log("Simulating logout in TEST_MODE");
        window.location.href = '/login.html';
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/user/logout`, {
            method: 'POST',
            credentials: 'include',
        });

        if (response.ok) {
            console.log("Logout successful");
            window.location.href = '/login.html';
        } else {
            console.error('Logout failed on the server.');
        }
    } catch (error) {
        console.error('Logout failed:', error);
    }
}