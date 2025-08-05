// src/components/AssignTalkForm.tsx
import React, { useState } from 'react';
import type { TalkAssignmentCreate } from '../client/types.gen';

interface AssignTalkFormProps {
    talkId: number; // The ID of the talk to assign
    onSave: (assignment: TalkAssignmentCreate) => void;
    onCancel: () => void;
    isSaving: boolean;
    // You might pass a list of members here for a dropdown
    // availableMembers: { id: number; name: string }[];
}


const AssignTalkForm: React.FC<AssignTalkFormProps> = ({
    talkId,
    onSave,
    onCancel,
    isSaving,
    // availableMembers, // This is optional
}) => {
    const [memberId, setMemberId] = useState<number | ''>('');
    const [roleId, setRoleId] = useState<number | ''>(''); // <-- New state for roleId

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Check for both memberId and roleId
        if (!memberId || !roleId) {
            alert('Please select a member and a role.');
            return;
        }

        onSave({
            talk_id: talkId,
            member_id: memberId as number,
            role_id: roleId as number, // <-- Pass the roleId
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 max-w-xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-4">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Assign Talk to Member</h3>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Member</label>
                <input
                    type="number"
                    value={memberId}
                    onChange={(e) => setMemberId(Number(e.target.value) || '')}
                    className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                    placeholder="Enter Member ID"
                    required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Role</label>
                <input
                    type="number"
                    value={roleId}
                    onChange={(e) => setRoleId(Number(e.target.value) || '')}
                    className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                    placeholder="Enter Role ID"
                    required
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
                    className="px-6 py-2 bg-purple-600 text-white rounded-md font-semibold hover:bg-purple-700 transition-colors disabled:bg-purple-400"
                    disabled={isSaving}
                >
                    {isSaving ? 'Assigning...' : 'Assign Talk'}
                </button>
            </div>
        </form>
    );
};

export default AssignTalkForm;