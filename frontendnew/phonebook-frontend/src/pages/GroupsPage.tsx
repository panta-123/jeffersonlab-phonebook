// pages/GroupsPage.tsx
import React, { useEffect, useState } from 'react';
import { workingGroupsListGroups, workingGroupsListGroupMembersOfGroup } from '../client/sdk.gen';
import type { GroupLiteResponse, GroupMemberResponse } from '../client/types.gen';
import { useAuth } from '../context/AuthContext';

const GroupsPage: React.FC = () => {
    const { user, isAuthenticated, isLoading: authLoading } = useAuth();
    const [groups, setGroups] = useState<GroupLiteResponse[]>([]);
    const [selectedGroup, setSelectedGroup] = useState<GroupLiteResponse | null>(null);
    const [groupMembers, setGroupMembers] = useState<GroupMemberResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [loadingMembers, setLoadingMembers] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [membersError, setMembersError] = useState<string | null>(null);

    // Effect to fetch the list of all groups
    useEffect(() => {
        const fetchGroups = async () => {
            setLoading(true);
            setError(null);
            try {
                const apiResponse = await workingGroupsListGroups();
                if ('status' in apiResponse && apiResponse.status === 200) {
                    setGroups(apiResponse.data || []);
                } else {
                    setError('Failed to load groups: ' + (apiResponse as any).error?.detail || 'Unknown error');
                }
            } catch (err) {
                console.error('Failed to fetch groups:', err);
                setError('Failed to load groups due to a network or unexpected error. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        if (!authLoading && isAuthenticated) {
            fetchGroups();
        }
    }, [isAuthenticated, authLoading]);

    // Effect to fetch members of the selected group
    useEffect(() => {
        const fetchGroupMembers = async () => {
            if (!selectedGroup) return;

            setLoadingMembers(true);
            setMembersError(null);
            try {
                const apiResponse = await workingGroupsListGroupMembersOfGroup({
                    path: {
                        group_id: selectedGroup.id
                    }
                });
                if ('status' in apiResponse && apiResponse.status === 200) {
                    setGroupMembers(apiResponse.data || []);
                } else {
                    setMembersError('Failed to load group members: ' + (apiResponse as any).error?.detail || 'Unknown error');
                }
            } catch (err) {
                console.error('Failed to fetch group members:', err);
                setMembersError('Failed to load group members due to a network or unexpected error.');
            } finally {
                setLoadingMembers(false);
            }
        };

        if (selectedGroup) {
            fetchGroupMembers();
        } else {
            // Clear members list when no group is selected
            setGroupMembers([]);
        }
    }, [selectedGroup]);

    // Render loading state for API data fetch OR auth status check
    if (loading || authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-lg text-gray-700">Loading groups data...</p>
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

    // Main content
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center p-4">
            <div className="container mx-auto mt-8 p-6 bg-white rounded-lg shadow-xl">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">Collaboration Working Groups</h1>

                {/* Display user info if available from the context */}
                {user && (
                    <p className="text-lg text-gray-600 mb-8 text-center">
                        Logged in as: <span className="font-semibold text-purple-600">{user.name || user.email}</span>
                        {user.isadmin && <span className="ml-2 text-sm text-green-600">(Admin)</span>}
                    </p>
                )}

                {groups.length === 0 ? (
                    <p className="text-center text-lg text-gray-600">No working groups found.</p>
                ) : (
                    <div className="flex flex-col md:flex-row gap-6">
                        {/* List of Groups */}
                        <div className="w-full md:w-1/3">
                            <h2 className="text-2xl font-bold text-gray-700 mb-4">Groups</h2>
                            <ul className="bg-gray-50 rounded-lg shadow-md p-4">
                                {groups.map((group) => (
                                    <li
                                        key={group.id}
                                        onClick={() => setSelectedGroup(group)}
                                        className={`py-3 px-4 rounded-lg cursor-pointer transition-colors duration-200 ${selectedGroup?.id === group.id ? 'bg-blue-200 text-blue-800 font-bold' : 'hover:bg-gray-100'
                                            }`}
                                    >
                                        {group.name}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* Group Members List */}
                        <div className="w-full md:w-2/3">
                            {selectedGroup ? (
                                <>
                                    <h2 className="text-2xl font-bold text-gray-700 mb-4">Members of {selectedGroup.name}</h2>
                                    {loadingMembers ? (
                                        <p className="text-gray-600">Loading members...</p>
                                    ) : membersError ? (
                                        <p className="text-red-600 font-semibold">{membersError}</p>
                                    ) : groupMembers.length === 0 ? (
                                        <p className="text-gray-600">No members found in this group.</p>
                                    ) : (
                                        <div className="overflow-x-auto w-full">
                                            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
                                                <thead>
                                                    <tr className="bg-gray-100 border-b border-gray-200">
                                                        <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Member Name</th>
                                                        <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                                                        <th className="py-3 px-6 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Institution</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {groupMembers.map((gm) => (
                                                        <tr key={gm.id} className="border-b border-gray-100 hover:bg-gray-50">
                                                            <td className="py-4 px-6 text-sm font-medium text-gray-900">{gm.member.first_name} {gm.member.last_name}</td>
                                                            <td className="py-4 px-6 text-sm text-gray-700">{gm.role.name}</td>
                                                            <td className="py-4 px-6 text-sm text-gray-700">{gm.member.institution?.short_name || 'N/A'}</td>
                                                        </tr>
                                                    ))}
                                                </tbody>
                                            </table>
                                        </div>
                                    )}
                                </>
                            ) : (
                                <div className="p-6 text-center text-lg text-gray-600 border-2 border-dashed border-gray-300 rounded-lg h-full flex items-center justify-center">
                                    Please select a group to view its members.
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default GroupsPage;