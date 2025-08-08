import React, { useEffect, useState } from 'react';
import {
    conferencesListConferences,
    conferencesGetConference,
    conferencesUpdateConference,
    conferencesCreateConference, // <-- New import
    talksCreateTalk,             // <-- New import
    talkAssignmentsCreateTalkAssignment // <-- New import
} from '../client/sdk.gen';

import type {
    ConferenceResponse,
    ConferenceLiteResponse,
    ConferenceUpdate,
    ConferenceCreate,             // <-- New import
    TalkCreate,                   // <-- New import
    TalkAssignmentCreate          // <-- New import
} from '../client/types.gen';

import { useAuth } from '../context/AuthContext';
import EditConferenceForm from '../components/EditConferenceForm';
import AddConferenceForm from '../components/AddConferenceForm';      // <-- New import
import AddTalkForm from '../components/AddTalkForm';                  // <-- New import
import AssignTalkForm from '../components/AssignTalkForm';            // <-- New import

const ConferencePage: React.FC = () => {
    const { user, isAuthenticated, isLoading: authLoading } = useAuth();

    // States
    const [conferences, setConferences] = useState<ConferenceLiteResponse[]>([]);
    const [selectedConference, setSelectedConference] = useState<ConferenceResponse | null>(null);
    const [editingConference, setEditingConference] = useState<ConferenceLiteResponse | null>(null);
    const [addingNewConference, setAddingNewConference] = useState<boolean>(false); // <-- New state
    const [addingNewTalk, setAddingNewTalk] = useState<boolean>(false); // <-- New state
    const [assigningTalkId, setAssigningTalkId] = useState<number | null>(null); // <-- New state
    const [loadingConferences, setLoadingConferences] = useState<boolean>(true);
    const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
    const [isSaving, setIsSaving] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch lite conferences list
    const fetchConferences = async () => {
        setLoadingConferences(true);
        try {
            const lite = await conferencesListConferences({ query: { skip: 0, limit: 100 } });
            if ('status' in lite && lite.status === 200 && lite.data) {
                const parsedConfs: ConferenceLiteResponse[] = lite.data.map(conf => ({
                    ...conf,
                    start_date: new Date(conf.start_date),
                    end_date: conf.end_date ? new Date(conf.end_date) : null,
                }));
                setConferences(parsedConfs);
            } else {
                setError('Failed to fetch conferences');
            }
        } catch (err) {
            setError('Unexpected error fetching conferences.');
        } finally {
            setLoadingConferences(false);
        }
    };


    // Fetch full conference details including talks
    const fetchConferenceDetails = async (conferenceId: number) => {
        setLoadingDetails(true);
        setError(null);
        try {
            const full = await conferencesGetConference({
                path: { conference_id: conferenceId },
                query: { include_talks: true }
            });
            if ('status' in full && full.status === 200 && full.data) {
                const parsedConference: ConferenceResponse = {
                    ...full.data,
                    start_date: new Date(full.data.start_date),
                    end_date: full.data.end_date ? new Date(full.data.end_date) : null,
                    talks: full.data.talks?.map(talk => ({
                        ...talk,
                        start_date: new Date(talk.start_date),
                        end_date: talk.end_date ? new Date(talk.end_date) : null
                    }))
                };
                setSelectedConference(parsedConference);
                setAddingNewTalk(false); // Hide the add talk form when details load
            } else {
                setError('Failed to fetch conference details');
            }
        } catch (err) {
            setError('Unexpected error fetching conference details.');
        } finally {
            setLoadingDetails(false);
        }
    };

    // Load conferences on auth success
    useEffect(() => {
        if (!authLoading && isAuthenticated) {
            fetchConferences();
        }
    }, [isAuthenticated, authLoading]);

    // Handle editing an existing conference
    const handleEdit = (conf: ConferenceLiteResponse | ConferenceResponse) => {
        setEditingConference(conf);
        setSelectedConference(null);
        setAddingNewConference(false);
        setAddingNewTalk(false);
    };

    const handleCancelEdit = () => {
        setEditingConference(null);
    };

    const handleSave = async (updatedConf: ConferenceLiteResponse) => {
        if (!updatedConf?.id) return;
        setIsSaving(true);
        setError(null);
        try {
            const payload: ConferenceUpdate = {
                name: updatedConf.name,
                location: updatedConf.location,
                start_date: updatedConf.start_date,
                end_date: updatedConf.end_date,
                url: updatedConf.url,
            };
            const response = await conferencesUpdateConference({
                path: { conference_id: updatedConf.id },
                body: payload
            });
            if ('status' in response && response.status === 200) {
                setEditingConference(null);
                await fetchConferences();
            } else {
                setError('Failed to update conference.');
            }
        } catch (err) {
            setError('Error saving conference.');
        } finally {
            setIsSaving(false);
        }
    };

    // Handle adding a new conference
    const handleAddNewConference = () => {
        setAddingNewConference(true);
        setSelectedConference(null);
        setEditingConference(null);
    };

    const handleCancelAdd = () => {
        setAddingNewConference(false);
    };

    const handleSaveNewConference = async (newConf: ConferenceCreate) => {
        setIsSaving(true);
        setError(null);
        try {
            const response = await conferencesCreateConference({
                body: newConf
            });
            if ('status' in response && (response.status === 200 || response.status === 201)) {
                setAddingNewConference(false);
                await fetchConferences();
            } else {
                setError('Failed to add new conference.');
            }
        } catch (err) {
            setError('Error adding new conference.');
        } finally {
            setIsSaving(false);
        }
    };

    // Handle adding a new talk
    const handleAddTalk = () => {
        setAddingNewTalk(true);
    };

    const handleCancelAddTalk = () => {
        setAddingNewTalk(false);
    };

    const handleSaveNewTalk = async (newTalk: TalkCreate) => {
        if (!selectedConference?.id) return;
        setIsSaving(true);
        setError(null);
        try {
            const response = await talksCreateTalk({
                body: newTalk
            });
            if ('status' in response && (response.status === 200 || response.status === 201)) {
                setAddingNewTalk(false);
                await fetchConferenceDetails(selectedConference.id);
            } else {
                setError('Failed to add new talk.');
            }
        } catch (err) {
            setError('Error adding new talk.');
        } finally {
            setIsSaving(false);
        }
    };

    // Handle assigning a talk to a member
    const handleAssignTalk = (talkId: number) => {
        setAssigningTalkId(talkId);
    };

    const handleCancelAssignTalk = () => {
        setAssigningTalkId(null);
    };

    const handleSaveTalkAssignment = async (assignment: TalkAssignmentCreate) => {
        if (!selectedConference?.id) return;
        setIsSaving(true);
        setError(null);
        try {
            const response = await talkAssignmentsCreateTalkAssignment({
                body: assignment
            });
            if ('status' in response && (response.status === 200 || response.status === 201)) {
                setAssigningTalkId(null);
                await fetchConferenceDetails(selectedConference.id);
            } else {
                setError('Failed to assign talk.');
            }
        } catch (err) {
            setError('Error assigning talk.');
        } finally {
            setIsSaving(false);
        }
    };

    // --- Conditional Rendering Logic ---
    if (loadingConferences || authLoading) {
        return <div className="p-6 text-center text-gray-700">Loading conferences...</div>;
    }

    if (error) {
        return <div className="text-center text-red-500 p-6">{error}</div>;
    }

    // Show EditConferenceForm if editing a conference
    if (editingConference) {
        return (
            <div className="p-6 max-w-2xl mx-auto">
                <EditConferenceForm
                    conference={editingConference}
                    onCancel={handleCancelEdit}
                    onSave={handleSave}
                    isSaving={isSaving}
                />
            </div>
        );
    }

    // Show AddConferenceForm if adding a new conference
    if (addingNewConference) {
        return (
            <div className="p-6 max-w-2xl mx-auto">
                <AddConferenceForm
                    onCancel={handleCancelAdd}
                    onSave={handleSaveNewConference}
                    isSaving={isSaving}
                />
            </div>
        );
    }

    // Show selected conference with talks and back button
    if (selectedConference) {
        return (
            <div className="p-6 max-w-6xl mx-auto">
                <button
                    onClick={() => setSelectedConference(null)}
                    className="mb-4 text-indigo-600 hover:underline"
                >
                    ← Back to conferences
                </button>
                <h1 className="text-3xl font-bold mb-4">{selectedConference.name}</h1>
                <p className="text-sm text-gray-500">{selectedConference.location}</p>
                <p className="text-sm text-gray-400">
                    {new Date(selectedConference.start_date).toLocaleDateString()}
                    {selectedConference.end_date && ` - ${new Date(selectedConference.end_date).toLocaleDateString()}`}
                </p>
                {selectedConference.url && (
                    <a href={selectedConference.url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:underline">
                        {selectedConference.url}
                    </a>
                )}
                <div className="flex justify-end mt-2">
                    {user?.isadmin && (
                        <>
                            <button
                                onClick={() => handleEdit(selectedConference)}
                                className="text-indigo-600 hover:text-indigo-800 font-semibold"
                            >
                                Edit Conference
                            </button>
                            <button
                                onClick={handleAddTalk}
                                className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700 transition-colors"
                            >
                                Add New Talk
                            </button>
                        </>
                    )}
                </div>

                {addingNewTalk && user?.isadmin && (
                    <div className="mt-4">
                        <AddTalkForm
                            conferenceId={selectedConference.id}
                            onCancel={handleCancelAddTalk}
                            onSave={handleSaveNewTalk}
                            isSaving={isSaving}
                        />
                    </div>
                )}

                <div className="mt-6">
                    <h2 className="text-xl font-semibold mb-2">Talks</h2>
                    {loadingDetails ? (
                        <p>Loading talks...</p>
                    ) : selectedConference.talks?.length ? (
                        <ul className="space-y-4">
                            {selectedConference.talks.map(talk => (
                                <li key={talk.id} className="border p-4 rounded bg-gray-50">
                                    <div className="font-semibold">{talk.title}</div>
                                    <div className="text-sm text-gray-500 mt-1">
                                        Date: {new Date(talk.start_date).toLocaleDateString()}
                                        {talk.end_date && ` - ${new Date(talk.end_date).toLocaleDateString()}`}
                                    </div>
                                    {talk.docdb_id && <div className="text-xs text-gray-400">DocDB: {talk.docdb_id}</div>}
                                    {talk.talk_link && (
                                        <a href={talk.talk_link} target="_blank" rel="noopener noreferrer" className="text-xs text-indigo-500 hover:underline">
                                            Talk Link
                                        </a>
                                    )}
                                    {talk.assignments?.length ? (
                                        <div className="mt-2">
                                            <h4 className="text-sm font-medium text-gray-700">Assigned Members:</h4>
                                            <ul className="list-disc list-inside ml-4 text-sm text-gray-600">
                                                {talk.assignments.map(assignment => (
                                                    <li key={assignment.id}>
                                                        {assignment.member?.first_name} {assignment.member?.last_name} ({assignment.role?.name})
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    ) : (
                                        <p className="text-xs text-gray-400 mt-2">No members assigned.</p>
                                    )}
                                    {user?.isadmin && (
                                        <button
                                            onClick={() => handleAssignTalk(talk.id)}
                                            className="ml-4 text-purple-600 hover:text-purple-800 font-semibold text-sm"
                                        >
                                            Assign to Member
                                        </button>
                                    )}
                                    {assigningTalkId === talk.id && user?.isadmin && (
                                        <AssignTalkForm
                                            talkId={talk.id}
                                            onCancel={handleCancelAssignTalk}
                                            onSave={handleSaveTalkAssignment}
                                            isSaving={isSaving}
                                        />
                                    )}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-gray-500">No talks assigned.</p>
                    )}
                </div>
            </div>
        );
    }

    // Render list of conferences by default
    return (
        <div className="p-6 max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold mb-4 text-center">Conferences</h1>
            {user?.isadmin && (
                <div className="flex justify-end mb-4">
                    <button
                        onClick={handleAddNewConference}
                        className="px-4 py-2 bg-green-600 text-white rounded-md font-semibold hover:bg-green-700 transition-colors"
                    >
                        Add New Conference
                    </button>
                </div>
            )}
            <div className="space-y-6">
                {conferences.map(conf => (
                    <div
                        key={conf.id}
                        className="bg-white shadow rounded-xl p-6 border border-gray-200 hover:bg-indigo-50 flex justify-between items-center"
                    >
                        <div onClick={() => fetchConferenceDetails(conf.id)} className="flex-1 cursor-pointer">
                            <h2 className="text-xl font-semibold">{conf.name}</h2>
                            {conf.location && <p className="text-sm text-gray-500">{conf.location}</p>}
                            <p className="text-sm text-gray-400">
                                {new Date(conf.start_date).toLocaleDateString()}
                                {conf.end_date && ` - ${new Date(conf.end_date).toLocaleDateString()}`}
                            </p>
                            {conf.url && (
                                <a href={conf.url} target="_blank" rel="noopener noreferrer" className="text-sm text-indigo-600 hover:underline" onClick={e => e.stopPropagation()}>
                                    {conf.url}
                                </a>
                            )}
                        </div>
                        {user?.isadmin && (
                            <button
                                onClick={e => {
                                    e.stopPropagation();
                                    handleEdit(conf);
                                }}
                                className="text-indigo-600 hover:text-indigo-800 font-semibold"
                            >
                                Edit
                            </button>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ConferencePage;