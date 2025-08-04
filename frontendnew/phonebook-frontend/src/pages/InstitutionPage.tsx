// pages/InstitutionPage.tsx
import React, { useEffect, useState } from 'react';
import { institutionsListInstitutions, institutionsUpdateInstitution } from '../client/sdk.gen';
import type { InstitutionLiteResponse, InstitutionUpdate } from '../client/types.gen';
import { useAuth } from '../context/AuthContext';
import EditInstitutionForm from '../components/EditInstitutionForm'; // Import the new component

const InstitutionPage: React.FC = () => {
    const { user, isAuthenticated, isLoading: authLoading } = useAuth();
    const [institutions, setInstitutions] = useState<InstitutionLiteResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [editingInstitution, setEditingInstitution] = useState<InstitutionLiteResponse | null>(null);
    const [isSaving, setIsSaving] = useState<boolean>(false);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const apiResponse = await institutionsListInstitutions({ query: { skip: 0, limit: 100 } });
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

    useEffect(() => {
        if (!authLoading && isAuthenticated) {
            fetchData();
        }
    }, [isAuthenticated, authLoading]);

    const handleEdit = (institution: InstitutionLiteResponse) => {
        setEditingInstitution(institution);
    };

    const handleCancelEdit = () => {
        setEditingInstitution(null);
    };

    const handleSave = async (updatedInstitution: InstitutionLiteResponse) => {
        if (!updatedInstitution || updatedInstitution.id === undefined) return;

        setIsSaving(true);
        try {
            // The API expects an InstitutionUpdate type, which has all optional fields.
            // We only need to send the fields that are being updated.
            const payload: InstitutionUpdate = {
                rorid: updatedInstitution.rorid,
            };

            const apiResponse = await institutionsUpdateInstitution({
                body: payload,
                path: { institution_id: updatedInstitution.id },
            });

            if ('status' in apiResponse && apiResponse.status === 200) {
                setEditingInstitution(null); // Close the edit form
                fetchData(); // Refresh the list of institutions
            } else {
                setError('Failed to update institution: ' + (apiResponse as any).error?.detail?.[0]?.msg || 'Unknown error');
            }
        } catch (err) {
            setError('Failed to update institution due to a network or unexpected error.');
        } finally {
            setIsSaving(false);
        }
    };

    if (loading || authLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <p className="text-lg text-gray-700">Loading institutions data...</p>
            </div>
        );
    }

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

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 flex flex-col items-center p-4">
            <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-6xl border border-gray-200">
                {editingInstitution ? (
                    // Render the EditInstitutionForm if an institution is being edited
                    <EditInstitutionForm
                        institution={editingInstitution}
                        onSave={handleSave}
                        onCancel={handleCancelEdit}
                        isSaving={isSaving}
                    />
                ) : (
                    // Otherwise, render the list of institutions
                    <div>
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
                                            {/* Add Actions column only for admins */}
                                            {user?.isadmin && <th className="border border-gray-300 px-4 py-2">Actions</th>}
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
                                                {/* Edit button visible only for admins */}
                                                {user?.isadmin && (
                                                    <td className="border border-gray-300 px-4 py-2">
                                                        <button
                                                            onClick={() => handleEdit(inst)}
                                                            className="text-indigo-600 hover:text-indigo-900 font-semibold"
                                                        >
                                                            Edit ROR ID
                                                        </button>
                                                    </td>
                                                )}
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default InstitutionPage;