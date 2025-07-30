import React from 'react'; // Removed useEffect, useState
import { Link, useNavigate } from 'react-router-dom';
import { signOut } from '../utils/auth'; // Only need signOut now
import type { AuthStatus } from '../client/types.gen';

// Define props interface for NavBar
interface NavBarProps {
    authStatus: AuthStatus | null; // Now accepts authStatus as a prop
    loadingAuth: boolean; // Add a loading state for auth status
}

const NavBar: React.FC<NavBarProps> = ({ authStatus, loadingAuth }) => { // Destructure props
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await signOut();
            // After successful logout, navigate to login.
            // The parent component (e.g., App.tsx) will handle updating its authStatus state
            // and re-rendering NavBar and other components.
            navigate('/login');
        } catch (error) {
            console.error("Logout failed:", error);
            alert("Failed to log out. Please try again."); // Simple feedback
        }
    };

    return (
        <nav className="bg-blue-800 p-4 shadow-md sticky top-0 z-50"> {/* Added sticky and z-50 */}
            <div className="container mx-auto flex justify-between items-center">
                {/* Logo or App Name */}
                <Link to="/" className="text-white text-2xl font-bold hover:text-blue-200 transition-colors duration-200">
                    JLab Phonebook
                </Link>

                {/* Navigation Links */}
                <div className="flex items-center space-x-6">
                    {/* Only show Dashboard link if authenticated */}
                    {authStatus?.authenticated && (
                        <Link to="/dashboard" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                            Dashboard
                        </Link>
                    )}
                    {/* Members Page Link */}
                    {authStatus?.authenticated && (
                        <Link to="/members" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                            Members
                        </Link>
                    )}
                    {/* Members Page Link */}
                    {authStatus?.authenticated && (
                        <Link to="/institutions" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                            Institutions
                        </Link>
                    )}
                    {/* Authentication Status & Buttons */}
                    {loadingAuth ? ( // Use loadingAuth prop
                        <span className="text-blue-300">Loading auth...</span>
                    ) : authStatus?.authenticated ? (
                        <>
                            <span className="text-white text-md">
                                Welcome, {authStatus.name || authStatus.email?.split('@')[0] || 'User'}
                            </span>
                            <button
                                onClick={handleLogout}
                                className="
                                    bg-red-600 text-white px-4 py-2 rounded-md font-semibold
                                    hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50
                                    transition-colors duration-300 ease-in-out
                                "
                            >
                                Logout
                            </button>
                        </>
                    ) : (
                        <Link
                            to="/login"
                            className="
                                bg-blue-600 text-white px-4 py-2 rounded-md font-semibold
                                hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
                                transition-colors duration-300 ease-in-out
                            "
                        >
                            Login
                        </Link>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default NavBar;