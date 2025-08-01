// pages/MembersPage.tsx
import React, { useEffect, useState } from 'react';
import { membersListMembers } from '../client/sdk.gen';
import type { MemberResponse } from '../client/types.gen';
import { useAuth } from '../context/AuthContext'; // Import the new hook

const MembersPage: React.FC = () => {
    const { user, isAuthenticated, isLoading: authLoading } = useAuth(); // Use the hook
    const [members, setMembers] = useState<MemberResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                const apiResponse = await membersListMembers();

                if (apiResponse.response.ok) {
                    setMembers(apiResponse.data || []);
                } else {
                    console.error('API call failed with status:', apiResponse.response.status, apiResponse.response.statusText);
                    console.error('API error details:', apiResponse.error);
                    setMembers([]);
                    setError(`Failed to load members: ${apiResponse.response.status} - ${apiResponse.response.statusText}`);
                }
            } catch (err) {
                console.error('Failed to fetch members (network or unexpected error):', err);
                setMembers([]);
                setError('Failed to load members due to a network or unexpected error. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        // Only fetch data if the user is authenticated and the auth status is no longer loading
        if (!authLoading && isAuthenticated) {
            fetchData();
        }
    }, [isAuthenticated, authLoading]); // Dependency on auth state

    // Render loading state for API data fetch OR auth status check
    if (loading || authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-lg text-gray-700">Loading members data...</p>
            </div>
        );
    }

    // Render error state
    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex flex-col items-center p-4">
                <div className="flex-grow flex items-center justify-center w-full">
                    <p className="text-xl text-red-700 font-semibold">{error}</p>
                </div>
            </div>
        );
    }

    // Render main content
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center p-4">
            <div className="container mx-auto mt-8 p-6 bg-white rounded-lg shadow-xl">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">Collaboration Members</h1>

                {/* Display user info if available from the context */}
                {user && (
                    <p className="text-lg text-gray-600 mb-8 text-center">
                        Logged in as: <span className="font-semibold text-purple-600">{user.name || user.email}</span>
                        {user.isadmin && <span className="ml-2 text-sm text-green-600">(Admin)</span>}
                    </p>
                )}

                {members.length === 0 ? (
                    <p className="text-center text-lg text-gray-600">No members found.</p>
                ) : (
                    <div className="overflow-x-auto w-full">
                        <table className="min-w-full bg-white border border-gray-200 rounded-lg">
                            <thead>
                                <tr className="bg-gray-100 border-b border-gray-200">
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution (Short)</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution (Full)</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date Joined</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                                </tr>
                            </thead>
                            <tbody>
                                {members.map((member) => (
                                    <tr key={member.id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-4 px-6 text-sm font-medium text-gray-900">{member.first_name} {member.last_name}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.email}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.institution?.short_name || 'N/A'}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.institution?.full_name || 'N/A'}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.date_joined}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.institution?.country || 'N/A'}</td>
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

export default MembersPage;