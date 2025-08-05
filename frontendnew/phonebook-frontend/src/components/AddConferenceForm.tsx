// src/components/AddConferenceForm.tsx
import React, { useState } from 'react';
import type { ConferenceCreate } from '../client/types.gen';

interface AddConferenceFormProps {
    onSave: (newConference: ConferenceCreate) => void;
    onCancel: () => void;
    isSaving: boolean;
}

const AddConferenceForm: React.FC<AddConferenceFormProps> = ({
    onSave,
    onCancel,
    isSaving,
}) => {
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(null);
    const [conferenceLink, setConferenceLink] = useState('');

    const formatDateForInput = (date: Date | null) => date ? date.toISOString().split('T')[0] : '';

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Basic validation
        if (!name || !startDate) {
            alert('Name and Start Date are required.'); // Consider a better UI for alerts
            return;
        }

        onSave({
            name,
            location,
            start_date: startDate,
            end_date: endDate,
            url: conferenceLink,
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Add New Conference</h2>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                    required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Conference URL</label>
                <input
                    type="url"
                    value={conferenceLink}
                    onChange={(e) => setConferenceLink(e.target.value)}
                    className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                />
            </div>

            <div className="flex space-x-4">
                <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                    <input
                        type="date"
                        value={formatDateForInput(startDate)}
                        onChange={(e) => setStartDate(e.target.value ? new Date(e.target.value) : null)}
                        className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                        required
                    />
                </div>

                <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                    <input
                        type="date"
                        value={formatDateForInput(endDate)}
                        onChange={(e) => setEndDate(e.target.value ? new Date(e.target.value) : null)}
                        className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                    />
                </div>
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
                    {isSaving ? 'Adding...' : 'Add Conference'}
                </button>
            </div>
        </form>
    );
};

export default AddConferenceForm;