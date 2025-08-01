// pages/InstitutionPage.tsx
import React, { useEffect, useState } from 'react';
import { institutionsListInstitutions } from '../client/sdk.gen';
import type { InstitutionResponse } from '../client/types.gen';
import { useAuth } from '../context/AuthContext'; // Import the new hook

const InstitutionPage: React.FC = () => {
    const { user, isAuthenticated, isLoading: authLoading } = useAuth(); // Use the hook
    const [institutions, setInstitutions] = useState<InstitutionResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                // The API call is now made directly
                const apiResponse = await institutionsListInstitutions({
                    query: { skip: 0, limit: 100 }
                });

                if ('status' in apiResponse && apiResponse.status === 200) {
                    setInstitutions(apiResponse.data || []);
                } else {
                    setError('Failed to load institutions: ' + (apiResponse as any).error?.detail?.[0]?.msg || 'Unknown error');
                }

            } catch (err) {
                setError('Failed to load institutions due to a network or unexpected error.');
            } finally {
                setLoading(false);
            }
        };

        // Only fetch data if the user is authenticated and the auth status is no longer loading
        if (!authLoading && isAuthenticated) {
            fetchData();
        }
    }, [isAuthenticated, authLoading]); // Dependency on auth state

    // Handle loading state for either auth or data fetching
    if (loading || authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-lg text-gray-700">Loading institutions data...</p>
            </div>
        );
    }

    // Handle error state
    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 flex flex-col items-center p-4">
                <div className="flex-grow flex items-center justify-center w-full">
                    <div className="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full text-center border border-gray-200">
                        <h1 className="text-4xl font-extrabold text-red-600 mb-6">Error</h1>
                        <p className="text-lg text-red-500 mb-4">{error}</p>
                        {user && (
                            <p className="text-md text-gray-500">
                                Logged in as: <span className="font-semibold text-purple-600">{user.email}</span>
                            </p>
                        )}
                    </div>
                </div>
            </div>
        );
    }

    // Render main content
    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 flex flex-col items-center p-4">
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-6xl border border-gray-200">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-6 text-center">Institutions</h1>

                {user && (
                    <p className="text-lg text-gray-600 mb-8 text-center">
                        Logged in as:{' '}
                        <span className="font-semibold text-purple-600">
                            {user.name || user.email}
                        </span>
                        {user.isadmin && (
                            <span className="ml-2 text-sm text-green-600">(Admin)</span>
                        )}
                    </p>
                )}

                {institutions.length === 0 ? (
                    <p className="text-center text-gray-700 text-xl">No institutions found.</p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="min-w-full table-auto border-collapse border border-gray-300 text-left">
                            <thead className="bg-indigo-100">
                                <tr>
                                    <th className="border border-gray-300 px-4 py-2">Full Name</th>
                                    <th className="border border-gray-300 px-4 py-2">Short Name</th>
                                    <th className="border border-gray-300 px-4 py-2">City</th>
                                    <th className="border border-gray-300 px-4 py-2">Country</th>
                                    <th className="border border-gray-300 px-4 py-2">Region</th>
                                    <th className="border border-gray-300 px-4 py-2">Active</th>
                                </tr>
                            </thead>
                            <tbody>
                                {institutions.map((inst) => (
                                    <tr key={inst.id} className="hover:bg-indigo-50">
                                        <td className="border border-gray-300 px-4 py-2">{inst.full_name}</td>
                                        <td className="border border-gray-300 px-4 py-2">{inst.short_name}</td>
                                        <td className="border border-gray-300 px-4 py-2">{inst.city}</td>
                                        <td className="border border-gray-300 px-4 py-2">{inst.country}</td>
                                        <td className="border border-gray-300 px-4 py-2">{inst.region || '-'}</td>
                                        <td className="border border-gray-300 px-4 py-2">
                                            {inst.is_active ? 'Yes' : 'No'}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default InstitutionPage;