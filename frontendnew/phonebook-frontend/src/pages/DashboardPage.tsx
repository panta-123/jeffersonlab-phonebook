// src/pages/DashboardPage.tsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Import the new hook

const DashboardPage: React.FC = () => {
    const navigate = useNavigate();
    const { user, isAuthenticated, isLoading } = useAuth(); // Use the hook to get auth state

    // The useEffect now only handles the redirect if the user isn't authenticated
    useEffect(() => {
        // We only check for a redirect once the loading state is false
        if (!isLoading && !isAuthenticated) {
            navigate('/login', { state: { from: location.pathname } });
        }
    }, [isLoading, isAuthenticated, navigate]);

    // Handle loading state
    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-xl text-gray-700">Loading dashboard...</p>
            </div>
        );
    }

    // This part should be unreachable due to the useEffect redirect,
    // but it's a good defensive practice.
    if (!isAuthenticated) {
        return null;
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
            <div className="bg-white p-8 rounded-lg shadow-xl text-center max-w-lg w-full">
                <h1 className="text-3xl font-bold text-blue-700 mb-4">
                    Welcome, {user?.name || user?.email?.split('@')[0] || 'User'}!
                </h1>
                <p className="text-lg text-gray-700 mb-6">
                    This is your dashboard. You are successfully logged in.
                </p>

                {user?.email && (
                    <p className="text-md text-gray-600 mb-2">
                        Your email: <span className="font-semibold">{user.email}</span>
                    </p>
                )}
                {user?.isadmin && ( // Changed from authStatus.isAdmin
                    <p className="text-md text-green-600 font-semibold mb-2">
                        (Administrator Privileges)
                    </p>
                )}
                {/* Add more dashboard content here */}
                <div className="mt-8">
                    <p className="text-gray-500">
                        Start exploring the JLab Phonebook application.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;