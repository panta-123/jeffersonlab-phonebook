// src/pages/DashboardPage.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { checkAuthStatus } from '../utils/auth'; // Import checkAuthStatus
import type { AuthStatus } from '../client/types.gen'; // Import AuthStatus type

const DashboardPage: React.FC = () => {
    const navigate = useNavigate();
    const [authStatus, setAuthStatus] = useState<AuthStatus | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const verifyAuth = async () => {
            try {
                const status = await checkAuthStatus();
                setAuthStatus(status);
                if (!status.authenticated) {
                    // If not authenticated, redirect to login page
                    navigate('/login', { state: { from: location } });
                }
            } catch (error) {
                console.error("Error verifying authentication on dashboard:", error);
                // In case of an error checking status, assume not authenticated
                navigate('/login', { state: { from: location } });
            } finally {
                setLoading(false);
            }
        };

        verifyAuth();
    }, [navigate]);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-xl text-gray-700">Loading dashboard...</p>
            </div>
        );
    }

    // If authStatus is null or not authenticated after loading, it means we've redirected
    // So this render should theoretically only happen if authenticated.
    // Added a defensive check anyway.
    if (!authStatus?.authenticated) {
        return null; // Or a fallback component, as a redirect should have occurred
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
            <div className="bg-white p-8 rounded-lg shadow-xl text-center max-w-lg w-full">
                <h1 className="text-3xl font-bold text-blue-700 mb-4">
                    Welcome, {authStatus.name || authStatus.email || 'User'}!
                </h1>
                <p className="text-lg text-gray-700 mb-6">
                    This is your dashboard. You are successfully logged in.
                </p>

                {authStatus.email && (
                    <p className="text-md text-gray-600 mb-2">
                        Your email: <span className="font-semibold">{authStatus.email}</span>
                    </p>
                )}
                {authStatus.isAdmin && (
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