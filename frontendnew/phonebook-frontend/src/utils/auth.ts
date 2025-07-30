// utils/auth.ts
// Import specific functions from sdk.gen.ts
import { userLogout, userCheckAuthStatus } from '../client/sdk.gen';
import type { AuthStatus } from '../client/types.gen';


// We won't directly manage a `currentUser` object here anymore,
// as the session will be managed by the backend (e.g., via cookies).

/**
 * Initiates the login process by redirecting to the backend's login endpoint.
 * The backend will then handle the redirection to the identity provider.
 */
export const signIn = async (): Promise<void> => {
    try {
        // You have two options here:
        // 1. Directly navigate the browser to the backend's login URL. This is the simplest for a direct redirect.
        window.location.href = "/api/v1/user/login";

        // 2. Call the generated function. If userLogin internally triggers a redirect, this works.
        //    However, usually the generated function would expect to return a response, not immediately redirect the browser.
        //    Given your backend handles the redirect, option 1 is generally more robust for this specific flow.
        // await userLogin(); // If userLogin returned a redirect, you might use this.

    } catch (error) {
        console.error("Error initiating sign-in:", error);
        throw new Error("Failed to initiate login process.");
    }
};

/**
 * Logs the user out by calling the backend's logout endpoint.
 * Assumes the backend clears the session cookie.
 */
export const signOut = async (): Promise<void> => {
    try {
        // Call the directly imported userLogout function
        await userLogout();
        console.log("Logout successful.");
        // Redirect to the login page or home page after logout
        window.location.href = "/login";
    } catch (error) {
        console.error("Error during sign-out:", error);
        throw new Error("Failed to log out.");
    }
};

/**
 * Checks the authentication status of the user by calling the backend's check-auth endpoint.
 * @returns A Promise that resolves with the authentication status, or rejects with an error.
 */
export const checkAuthStatus = async (): Promise<AuthStatus> => { // <--- ADD THIS EXPLICIT RETURN TYPE
    try {
        const apiResponse = await userCheckAuthStatus(); // Changed to apiResponse for consistency

        // Define a default unauthenticated status object
        const unauthenticatedStatus: AuthStatus = {
            authenticated: false,
            isAdmin: false,
            email: null, // Always provide null for optional fields if not present
            name: null,  // Always provide null for optional fields if not present
        };

        // Even though types.gen.ts says 200: AuthStatus, defensive check is still good.
        // The apiResponse.response.ok check ensures we received a 2xx HTTP status.
        if (apiResponse.response.ok && apiResponse.data) { // Check both HTTP status and data presence
            // If response.data is received, ensure optional fields are handled.
            return {
                ...unauthenticatedStatus, // Start with defaults
                ...apiResponse.data,         // Override with actual data
                // Explicitly handle potential undefined for optional fields from backend response
                email: apiResponse.data.email === undefined ? null : apiResponse.data.email,
                name: apiResponse.data.name === undefined ? null : apiResponse.data.name,
            };
        } else {
            // If response is not ok, or no data, return the unauthenticated status
            console.error("Authentication check failed or returned no data:", apiResponse.response.status, apiResponse.response.statusText, apiResponse.error);
            return unauthenticatedStatus;
        }
    } catch (error) {
        // This catch block handles network errors or unhandled exceptions
        console.error("Error checking authentication status (network/unexpected error):", error);
        // In case of any other error, return a default unauthenticated AuthStatus
        return { authenticated: false, isAdmin: false, email: null, name: null };
    }
};

// The initializeAuth function will now correctly inherit the Promise<AuthStatus> return type
export const initializeAuth = async () => {
    return await checkAuthStatus();
};