// utils/mockData.ts
import type { MemberResponse, InstitutionResponse, GroupResponse } from '../client/types.gen';

// --- Mock Institutions ---
const mockInstitution1: InstitutionResponse = {
    id: 1,
    full_name: "University of Northern Virginia",
    short_name: "UNOVA",
    country: "USA",
    region: "Virginia",
    city: "Fairfax",
    address: "123 University Blvd",
    date_added: "2020-01-01T00:00:00Z",
    is_active: true,
    latitude: 38.8462,
    longitude: -77.3064,
};

const mockInstitution2: InstitutionResponse = {
    id: 2,
    full_name: "Virginia Tech Institute",
    short_name: "VTI",
    country: "USA",
    region: "Virginia",
    city: "Blacksburg",
    address: "456 Tech Drive",
    date_added: "2019-05-10T00:00:00Z",
    is_active: true,
    latitude: 37.2296,
    longitude: -80.4230,
};

const mockInstitution3: InstitutionResponse = {
    id: 3,
    full_name: "Global Research Institute",
    short_name: "GRI",
    country: "Canada",
    region: "Ontario",
    city: "Toronto",
    address: "789 Research Ave",
    date_added: "2021-08-22T00:00:00Z",
    is_active: true,
    latitude: 43.6532,
    longitude: -79.3832,
};

// --- Mock Members ---
export const mockMembers: MemberResponse[] = [
    {
        id: 101,
        first_name: "Sarah",
        last_name: "Connor",
        email: "sarah.connor@unova.edu",
        orcid: "0000-0002-1234-5678",
        preferred_author_name: "S. Connor",
        institution_id: mockInstitution1.id,
        date_joined: "2023-01-15T10:00:00Z",
        date_left: null,
        is_active: true,
        experimental_data: { "level": "senior", "projects": ["Project A", "Project B"] },
        institution: mockInstitution1, // Nested institution object
    },
    {
        id: 102,
        first_name: "John",
        last_name: "Doe",
        email: "john.doe@vti.edu",
        orcid: null,
        preferred_author_name: null,
        institution_id: mockInstitution2.id,
        date_joined: "2022-03-20T14:30:00Z",
        date_left: null,
        is_active: true,
        experimental_data: {},
        institution: mockInstitution2,
    },
    {
        id: 103,
        first_name: "Emily",
        last_name: "White",
        email: "emily.white@gsi.org",
        orcid: "0000-0003-9876-5432",
        preferred_author_name: "E. White",
        institution_id: mockInstitution3.id,
        date_joined: "2024-02-01T08:00:00Z",
        date_left: null,
        is_active: true,
        experimental_data: { "role": "researcher" },
        institution: mockInstitution3,
    },
    {
        id: 104,
        first_name: "David",
        last_name: "Lee",
        email: "david.lee@example.com",
        orcid: null,
        preferred_author_name: "D. Lee",
        institution_id: 0, // No specific institution ID, or an ID not corresponding to mock institutions
        date_joined: "2021-07-25T11:45:00Z",
        date_left: "2024-06-30T17:00:00Z", // Example of a left member
        is_active: false, // Example of an inactive member
        experimental_data: null,
        institution: null, // Explicitly null institution for this member
    },
    {
        id: 105,
        first_name: "Maria",
        last_name: "Garcia",
        email: "maria.garcia@unova.edu",
        orcid: "0000-0001-1122-3344",
        preferred_author_name: null,
        institution_id: mockInstitution1.id,
        date_joined: "2024-07-28T16:40:00Z", // Today's date
        date_left: null,
        is_active: true,
        experimental_data: { "status": "new-hire" },
        institution: mockInstitution1,
    },
];

// --- Mock Groups (Example, based on GroupResponse type) ---
export const mockGroups: GroupResponse[] = [
    {
        id: 1,
        name: "Steering Committee",
    },
    {
        id: 2,
        name: "Working Group Alpha",
    },
    {
        id: 3,
        name: "Data Analysis Team",
    },
];

// You can add other mock data as needed, following the types from types.gen.ts
// e.g., mockInstitutions if you have an institutions page
export const mockInstitutions = [
    mockInstitution1,
    mockInstitution2,
    mockInstitution3,
    {
        id: 4,
        full_name: "Newport News University",
        short_name: "NNU",
        country: "USA",
        region: "Virginia",
        city: "Newport News",
        address: "1 University Way",
        date_added: "2022-10-01T00:00:00Z",
        is_active: true,
        latitude: 37.0673,
        longitude: -76.4950,
    },
];