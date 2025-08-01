// pages/LoginPage.tsx
import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Import the new hook

const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { isAuthenticated, isLoading, login } = useAuth(); // Use the hook

    // Effect to check if user is already authenticated
    useEffect(() => {
        // Only run after the initial loading check is complete
        if (!isLoading && isAuthenticated) {
            // If already authenticated, redirect to the page they were trying to reach
            const from = location.state?.from || "/dashboard";
            navigate(from, { replace: true });
        }
    }, [isAuthenticated, isLoading, navigate, location.state]);

    // Show a loading state while we check authentication status
    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-xl text-gray-700">Checking login status...</p>
            </div>
        );
    }

    // The login page content is only rendered if the user is not authenticated
    // The handleLogin function now uses the context's login function
    const handleLogin = () => {
        login(location.state?.from?.pathname || '/dashboard');
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 font-sans">
            <div className="bg-white p-10 rounded-lg shadow-xl text-center">
                <h2 className="mb-5 text-2xl font-semibold text-gray-800">
                    Welcome to the JLab Phonebook
                </h2>
                <p className="mb-8 text-gray-600">
                    Please log in to access the application.
                </p>
                <button
                    onClick={handleLogin}
                    className="
                        px-6 py-3 text-lg font-bold text-white bg-blue-600 rounded-md
                        hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
                        transition-colors duration-300 ease-in-out
                    "
                >
                    Login with JLab SSO
                </button>
            </div>
        </div>
    );
};

export default LoginPage;