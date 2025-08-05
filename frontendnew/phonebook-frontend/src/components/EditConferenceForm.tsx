import React, { useState, useEffect } from 'react';
import type { ConferenceResponse } from '../client/types.gen';

interface EditConferenceFormProps {
    conference: ConferenceResponse;
    onSave: (updatedConference: ConferenceResponse) => void;
    onCancel: () => void;
    isSaving: boolean;
}

const EditConferenceForm: React.FC<EditConferenceFormProps> = ({
    conference,
    onSave,
    onCancel,
    isSaving,
}) => {
    // Helper to format to YYYY-MM-DD
    const formatDateForInput = (date: Date | null) => date ? date.toISOString().split('T')[0] : '';
    const [name, setName] = useState(conference.name);
    const [location, setLocation] = useState(conference.location || '');
    const [startDate, setStartDate] = useState(conference.start_date);
    const [endDate, setEndDate] = useState(conference.end_date);
    // Correct way to declare state for the conference URL
    const [conferenceLink, setConferenceLink] = useState(conference.url || '');

    useEffect(() => {
        setName(conference.name);
        setLocation(conference.location || '');
        setStartDate(conference.start_date);
        setEndDate(conference.end_date);
        // Correctly set the state on conference change
        setConferenceLink(conference.url || '');
    }, [conference]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSave({
            ...conference,
            name,
            location,
            start_date: startDate,
            end_date: endDate,
            // Include the conferenceLink in the saved object
            url: conferenceLink,
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Edit Conference</h2>

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
                        onChange={(e) => setStartDate(new Date(e.target.value))}
                        className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                        required
                    />
                </div>

                <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                    <input
                        type="date"
                        value={formatDateForInput(endDate ?? null)}
                        onChange={(e) => setEndDate(new Date(e.target.value))}
                        className="w-full px-3 py-2 border rounded-md border-indigo-500 ring-2 ring-indigo-200"
                        required
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
                    {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
            </div>
        </form>
    );
};

export default EditConferenceForm;