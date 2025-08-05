import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Import the new hook

const NavBar: React.FC = () => {
    const { isAuthenticated, user, isLoading, logout } = useAuth(); // Use the hook to get auth state
    //#const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        // The logout function in AuthContext already handles the redirect, so no need for navigate here.
    };

    return (
        <nav className="bg-blue-800 p-4 shadow-md sticky top-0 z-50">
            <div className="container mx-auto flex justify-between items-center">
                <Link to="/" className="text-white text-2xl font-bold hover:text-blue-200 transition-colors duration-200">
                    JLab Phonebook
                </Link>

                <div className="flex items-center space-x-6">
                    {/* Only show these links if authenticated */}
                    {isAuthenticated && (
                        <>
                            <Link to="/dashboard" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                                Dashboard
                            </Link>
                            <Link to="/members" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                                Members
                            </Link>
                            <Link to="/institutions" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                                Institutions
                            </Link>
                            <Link to="/boards" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                                Boards
                            </Link>
                            <Link to="/groups" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                                Groups
                            </Link>
                            <Link to="/conferences" className="text-white text-lg hover:text-blue-200 transition-colors duration-200">
                                Conferences
                            </Link>
                        </>
                    )}

                    {/* Authentication Status & Buttons */}
                    {isLoading ? (
                        <span className="text-blue-300">Loading auth...</span>
                    ) : isAuthenticated ? (
                        <>
                            <span className="text-white text-md">
                                Welcome, {user?.name || user?.email?.split('@')[0] || 'User'}
                            </span>
                            <button
                                onClick={handleLogout}
                                className="bg-red-600 text-white px-4 py-2 rounded-md font-semibold hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors duration-300 ease-in-out"
                            >
                                Logout
                            </button>
                        </>
                    ) : (
                        <Link
                            to="/login"
                            className="bg-blue-600 text-white px-4 py-2 rounded-md font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-300 ease-in-out"
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