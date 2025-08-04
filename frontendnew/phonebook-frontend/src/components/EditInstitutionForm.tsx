// components/EditInstitutionForm.tsx
import React, { useState, useEffect } from 'react';
import type { InstitutionLiteResponse } from '../client/types.gen';

interface EditInstitutionFormProps {
    institution: InstitutionLiteResponse;
    onSave: (updatedInstitution: InstitutionLiteResponse) => void;
    onCancel: () => void;
    isSaving: boolean;
}

const EditInstitutionForm: React.FC<EditInstitutionFormProps> = ({ institution, onSave, onCancel, isSaving }) => {
    // State to hold only the editable rorid
    const [rorid, setRorid] = useState<string | null | undefined>(institution.rorid);

    // Update the state if the institution prop changes
    useEffect(() => {
        setRorid(institution.rorid);
    }, [institution]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRorid(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Create an object with the updated rorid and all other original data
        const updatePayload = {
            ...institution,
            rorid: rorid,
        };
        onSave(updatePayload);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Update ROR ID</h2>

            {/* Read-Only Full Name */}
            <div>
                <label className="block text-gray-700 font-bold mb-1">Institution</label>
                <p className="w-full px-3 py-2 border rounded-md bg-gray-100 text-gray-800">
                    {institution.full_name}
                </p>
            </div>

            {/* Editable ROR ID Field */}
            <div>
                <label className="block text-gray-700 font-bold mb-1">ROR ID</label>
                <input
                    type="text"
                    name="rorid"
                    value={rorid || ''}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                    placeholder="Enter ROR ID"
                />
            </div>

            <div className="flex justify-end space-x-4 mt-6">
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 font-semibold hover:bg-gray-100 transition-colors"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    className="px-6 py-2 bg-indigo-600 text-white rounded-md font-semibold hover:bg-indigo-700 transition-colors disabled:bg-indigo-400"
                    disabled={isSaving}
                >
                    {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
            </div>
        </form>
    );
};

export default EditInstitutionForm;