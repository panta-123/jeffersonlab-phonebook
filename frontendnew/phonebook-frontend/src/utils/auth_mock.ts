// utils/auth.ts
// Import specific functions from sdk.gen.ts
import { userLogout, userCheckAuthStatus } from '../client/sdk.gen';

// You will need to install jwt-decode: npm install jwt-decode or yarn add jwt-decode
import { jwtDecode } from 'jwt-decode';

// --- SIMULATION CONFIGURATION ---
export const SIMULATE_AUTH = true; // Set to true to enable simulation, false for actual backend calls

// Manually put your simulated JWT here.
// You can generate one at jwt.io. Ensure the payload mimics what your backend would send.
// Example payload for this dummy token:
// { "sub": "1234567890", "name": "Dev User", "email": "dev@example.com", "isAdmin": true, "authenticated": true, "iat": 1516239022, "exp": 2967528000 }
// (exp is far in the future, e.g., year 2060)
const MANUAL_SIMULATED_JWT = SIMULATE_AUTH ? "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJodHRwOi8vY2lsb2dvbi5vcmcvc2VydmVyRS91c2Vycy8xMDg1MDYiLCJlbWFpbCI6InBhbnRhQGpsYWIub3JnIiwibmFtZSI6IkFuaWwgUGFudGEiLCJpc2FkbWluIjp0cnVlLCJleHAiOjE3NTM3MzkyMDR9.8km8zmA02zcsk71oUWU61anK0s7fr5bl5KAXvIRGz0k" : null;
// --- END SIMULATION CONFIGURATION ---

/**
 * Initiates the login process by redirecting to the backend's login endpoint.
 * The backend will then handle the redirection to the identity provider.
 */
export const signIn = async (): Promise<void> => {
    if (SIMULATE_AUTH) {
        console.log("SIMULATION MODE: Simulating sign-in. Redirecting to dashboard.");
        // In simulation, we don't interact with the backend login endpoint.
        // We're just "pretending" to be logged in by relying on MANUAL_SIMULATED_JWT
        // being present for checkAuthStatus.
        window.location.href = "/dashboard"; // Redirect to a page that assumes login success
    } else {
        try {
            window.location.href = "/api/v1/user/login";
        } catch (error) {
            console.error("Error initiating sign-in:", error);
            throw new Error("Failed to initiate login process.");
        }
    }
};

/**
 * Logs the user out by calling the backend's logout endpoint.
 * Assumes the backend clears the session cookie.
 */
export const signOut = async (): Promise<void> => {
    if (SIMULATE_AUTH) {
        console.log("SIMULATION MODE: Simulating sign-out. No backend call.");
        // In simulation, we just redirect to the login page.
        // The checkAuthStatus will then return unauthenticated because MANUAL_SIMULATED_JWT
        // is always there, but we're simulating the *state* of being logged out by redirecting.
        window.location.href = "/login";
    } else {
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
    }
};

/**
 * Checks the authentication status of the user.
 * @returns A Promise that resolves with the authentication status, or rejects with an error.
 */
export const checkAuthStatus = async () => {
    if (SIMULATE_AUTH && MANUAL_SIMULATED_JWT) {
        console.log("SIMULATION MODE: Checking auth status using manual JWT.");
        try {
            const decodedToken: any = jwtDecode(MANUAL_SIMULATED_JWT);
            // Optional: Check expiration for a more robust simulation
            const currentTime = Date.now() / 1000;
            if (decodedToken.exp && decodedToken.exp < currentTime) {
                console.warn("Simulated JWT has expired. Consider updating MANUAL_SIMULATED_JWT.");
                return { authenticated: false, isAdmin: false, email: null, name: null };
            }

            return {
                authenticated: decodedToken.authenticated || true, // Assume true if token is valid
                isAdmin: decodedToken.isAdmin || true,
                email: decodedToken.email || null,
                name: decodedToken.name || null
            };
        } catch (decodeError) {
            console.error("Error decoding MANUAL_SIMULATED_JWT. Is it valid?", decodeError);
            return { authenticated: false, isAdmin: false, email: null, name: null };
        }
    } else {
        try {
            // Call the directly imported userCheckAuthStatus function
            const response = await userCheckAuthStatus();
            return response.data; // Assuming response.data contains the AuthStatus object
        } catch (error) {
            console.error("Error checking authentication status:", error);
            // If the check fails (e.g., 401 Unauthorized), assume not authenticated
            return { authenticated: false, isAdmin: false, email: null, name: null };
        }
    }
};

// The initializeAuth function can now use checkAuthStatus
export const initializeAuth = async () => {
    return await checkAuthStatus();
};