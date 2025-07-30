// pages/LoginPage.tsx
import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { checkAuthStatus } from '../utils/auth';

const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();

    // Function to handle the login click
    const handleLogin = () => {
        // Correct way to navigate to the backend's login endpoint.
        // We're expecting the backend to handle the redirect to the IdP.
        window.location.href = "/api/v1/user/login";
    };

    // Effect to check authentication status on component mount
    useEffect(() => {
        const checkAuth = async () => {
            const authStatus = await checkAuthStatus();
            if (authStatus.authenticated) {
                // If already authenticated, redirect to dashboard or intended page
                const from = location.state?.from?.pathname || "/dashboard";
                navigate(from, { replace: true });
            }
        };

        checkAuth();
    }, [navigate, location]);

    return (
        <div
            className="flex flex-col items-center justify-center min-h-screen bg-gray-100 font-sans"
        >
            <div
                className="bg-white p-10 rounded-lg shadow-xl text-center"
            >
                <h2
                    className="mb-5 text-2xl font-semibold text-gray-800"
                >
                    Welcome to the JLab Phonebook
                </h2>
                <p
                    className="mb-8 text-gray-600"
                >
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