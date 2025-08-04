// pages/BoardMembersPage.tsx
import React, { useEffect, useState } from 'react';
import { boardMembersListBoardMemberships } from '../client/sdk.gen';
import type { InstitutionalBoardMemberResponse } from '../client/types.gen';
import { useAuth } from '../context/AuthContext';

// Define the BoardType enum based on your API schema
type BoardType = 'institutional' | 'executive';

const BoardMembersPage: React.FC = () => {
    const { isAuthenticated, isLoading: authLoading } = useAuth();
    const [boardMemberships, setBoardMemberships] = useState<InstitutionalBoardMemberResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    // State for filter parameters
    const [filterBoardType, setFilterBoardType] = useState<BoardType | ''>('');
    const [filterMemberId, setFilterMemberId] = useState<string>('');
    const [filterInstitutionId, setFilterInstitutionId] = useState<string>('');

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);

            // Exit early if not authenticated
            if (!isAuthenticated) {
                setLoading(false);
                return;
            }

            try {
                // Construct the query parameters
                const params = {
                    board_type: filterBoardType === 'institutional' || filterBoardType === 'executive' ? filterBoardType : undefined,
                    member_id: filterMemberId ? parseInt(filterMemberId, 10) : undefined,
                    institution_id: filterInstitutionId ? parseInt(filterInstitutionId, 10) : undefined,
                };

                // Remove undefined values to prevent them from being sent in the URL
                const cleanedParams = Object.fromEntries(
                    Object.entries(params).filter(([, v]) => v !== undefined)
                );
                console.log('cleanedParams:', cleanedParams)
                console.log('params:', params)
                const apiResponse = await boardMembersListBoardMemberships({ params: cleanedParams });

                if ('status' in apiResponse && apiResponse.status === 200) {
                    setBoardMemberships(apiResponse.data || []);
                } else {
                    setError('Failed to load board memberships: ' + (apiResponse as any).error?.detail?.[0]?.msg || 'Unknown error');
                }
            } catch (err) {
                console.error('Failed to fetch board memberships:', err);
                setBoardMemberships([]);
                setError('Failed to load board members due to an unexpected error. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        if (!authLoading) {
            fetchData();
        }
    }, [isAuthenticated, authLoading, filterBoardType, filterMemberId, filterInstitutionId]);

    // Render loading state
    if (loading || authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-lg text-gray-700">Loading board members data...</p>
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

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center p-4">
            <div className="container mx-auto mt-8 p-6 bg-white rounded-lg shadow-xl">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-6 text-center">Board Memberships</h1>

                {/* Filter Controls */}
                <div className="mb-8 flex flex-wrap gap-4 justify-center">
                    <div className="flex flex-col">
                        <label htmlFor="board-type-filter" className="text-sm font-medium text-gray-700 mb-1">Filter by Board Type:</label>
                        <select
                            id="board-type-filter"
                            value={filterBoardType}
                            onChange={(e) => setFilterBoardType(e.target.value as BoardType | '')}
                            className="p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                            <option value="">All</option>
                            <option value="institutional">Institutional</option>
                            <option value="executive">Executive</option>
                        </select>
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="member-id-filter" className="text-sm font-medium text-gray-700 mb-1">Filter by Member ID:</label>
                        <input
                            id="member-id-filter"
                            type="number"
                            value={filterMemberId}
                            onChange={(e) => setFilterMemberId(e.target.value)}
                            className="p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            placeholder="e.g., 123"
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="institution-id-filter" className="text-sm font-medium text-gray-700 mb-1">Filter by Institution ID:</label>
                        <input
                            id="institution-id-filter"
                            type="number"
                            value={filterInstitutionId}
                            onChange={(e) => setFilterInstitutionId(e.target.value)}
                            className="p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            placeholder="e.g., 456"
                        />
                    </div>
                </div>

                {boardMemberships.length === 0 ? (
                    <p className="text-center text-lg text-gray-600">No board memberships found with the current filters.</p>
                ) : (
                    <div className="overflow-x-auto w-full">
                        <table className="min-w-full bg-white border border-gray-200 rounded-lg">
                            <thead>
                                <tr className="bg-gray-100 border-b border-gray-200">
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Member Name</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Board Type</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                                    <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date Started</th>
                                </tr>
                            </thead>
                            <tbody>
                                {boardMemberships.map((membership) => (
                                    <tr key={membership.id} className="border-b border-gray-100 hover:bg-gray-50">
                                        <td className="py-4 px-6 text-sm font-medium text-gray-900">
                                            {membership.member?.first_name} {membership.member?.last_name}
                                        </td>
                                        <td className="py-4 px-6 text-sm text-gray-700">
                                            {membership.institution?.short_name || 'N/A'}
                                        </td>
                                        <td className="py-4 px-6 text-sm text-gray-700">
                                            {membership.board_type}
                                        </td>
                                        <td className="py-4 px-6 text-sm text-gray-700">
                                            {membership.role?.name || 'N/A'}
                                        </td>
                                        <td className="py-4 px-6 text-sm text-gray-700">
                                            {membership.start_date instanceof Date
                                                ? membership.start_date.toLocaleDateString()
                                                : new Date(membership.start_date).toLocaleDateString()}
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

export default BoardMembersPage;