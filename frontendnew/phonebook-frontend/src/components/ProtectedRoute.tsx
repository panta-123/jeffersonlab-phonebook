// components/ProtectedRoute.tsx
import React, { useEffect, useState } from 'react';
import { initializeAuth } from '../utils/auth';
import { Navigate } from 'react-router-dom';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    // State to hold authentication status (true/false/null for loading)
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
    // Removed authStatus state if it's not used directly by ProtectedRoute

    useEffect(() => {
        const checkAuthentication = async () => {
            const status = await initializeAuth(); // This returns an AuthStatus object
            setIsAuthenticated(status.authenticated);
            // We no longer store the full 'status' in a state variable here if not used
        };

        checkAuthentication();
    }, []);

    if (isAuthenticated === null) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-lg text-gray-700">Checking authentication...</p>
            </div>
        );
    }

    return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;