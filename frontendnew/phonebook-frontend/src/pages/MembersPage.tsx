import React, { useEffect, useState } from 'react';
import { membersListMembers } from '../client/sdk.gen';
import type { PaginatedMemberResponse, MemberLiteResponse } from '../client/types.gen';
import { useAuth } from '../context/AuthContext';

const MembersPage: React.FC = () => {
    const { isAuthenticated, isLoading: authLoading, user } = useAuth();
    const [paginatedResponse, setPaginatedResponse] = useState<PaginatedMemberResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    // Pagination states
    const [currentPage, setCurrentPage] = useState<number>(0);
    const limit = 10;

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            try {
                const apiResponse = await membersListMembers({ query: { skip: currentPage * limit, limit } });
                if (apiResponse.status === 200 && apiResponse.data) {
                    setPaginatedResponse(apiResponse.data);
                } else {
                    const errorMessage = (apiResponse as any).error?.detail?.[0]?.msg || (apiResponse as any).error?.message || 'Unknown API error';
                    setError('Failed to load members: ' + errorMessage);
                    setPaginatedResponse(null);
                }
            } catch (err) {
                console.error('Failed to fetch members:', err);
                setError('Failed to load members due to a network or unexpected error. Please try again later.');
                setPaginatedResponse(null);
            } finally {
                setLoading(false);
            }
        };

        if (!authLoading && isAuthenticated) {
            fetchData();
        }
    }, [isAuthenticated, authLoading, currentPage, limit]);

    const handleNextPage = () => {
        if (paginatedResponse && (currentPage + 1) * limit < paginatedResponse.total) {
            setCurrentPage(prevPage => prevPage + 1);
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 0) {
            setCurrentPage(prevPage => prevPage - 1);
        }
    };

    if (loading) {
        return <div className="p-6 text-center text-gray-700">Loading members...</div>;
    }

    if (error) {
        return <div className="text-center text-red-500 p-6">{error}</div>;
    }

    const members: MemberLiteResponse[] = paginatedResponse?.items || [];
    const totalMembers = paginatedResponse?.total || 0;
    const canGoNext = (currentPage + 1) * limit < totalMembers;
    const canGoPrevious = currentPage > 0;

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center p-4">
            <div className="container mx-auto mt-8 p-6 bg-white rounded-lg shadow-xl">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">Collaboration Members</h1>

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
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ORCID</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution (Short)</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution (Full)</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date Joined</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">isActive</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                                </tr>
                            </thead>
                            <tbody>
                                {members.map((member) => (
                                    <tr key={member.id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-4 px-6 text-sm font-medium text-gray-900">{member.first_name} {member.last_name}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.email}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.orcid}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.institution?.short_name || 'N/A'}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.institution?.full_name || 'N/A'}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">
                                            {member.date_joined instanceof Date
                                                ? member.date_joined.toLocaleDateString()
                                                : new Date(member.date_joined).toLocaleDateString()}
                                        </td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.is_active}</td>
                                        <td className="py-4 px-6 text-sm text-gray-700">{member.institution?.country || 'N/A'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
                {/* Pagination Controls */}
                {totalMembers > limit && (
                    <div className="flex justify-between items-center mt-6">
                        <button
                            onClick={handlePreviousPage}
                            disabled={!canGoPrevious}
                            className={`px-4 py-2 rounded-md font-semibold ${canGoPrevious ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-gray-300 text-gray-600 cursor-not-allowed'}`}
                        >
                            Previous
                        </button>
                        <span className="text-gray-700">Page {currentPage + 1} of {Math.ceil(totalMembers / limit)}</span>
                        <button
                            onClick={handleNextPage}
                            disabled={!canGoNext}
                            className={`px-4 py-2 rounded-md font-semibold ${canGoNext ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-gray-300 text-gray-600 cursor-not-allowed'}`}
                        >
                            Next
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MembersPage;