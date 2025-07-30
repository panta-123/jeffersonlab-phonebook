export interface User {
    uid: string;    // Unique identifier for the user
    email: string;  // User's email address
    // Add more properties as needed, e.g.:
    // name?: string;
    // role?: 'admin' | 'member';
    // lastLogin?: Date;
}

export interface Institution {
    id: number;
    full_name: string;
    short_name: string;
    country: string;
    region: string | null;
    latitude: number | null;
    longitude: number | null;
    city: string | null;
    address: string | null;
    date_added: string; // ISO date string
    date_removed: string | null; // ISO date string
    is_active: boolean;
}

export interface Member {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    orcid: string | null;
    preferred_author_name: string | null;
    institution_id: number;
    date_joined: string; // ISO date string
    date_left: string | null; // ISO date string
    is_active: boolean;
    experimental_data: Record<string, any> | null;
    // Frontend-only properties for display, if you fetch the full institution object
    institution_name?: string;
}

export interface MemberInstitutionHistory {
    id: number;
    member_id: number;
    institution_id: number;
    start_date: string; // ISO date string
    end_date: string | null; // ISO date string
}

export interface Group {
    id: number;
    name: string;
}

export interface GroupMember {
    id: number;
    group_id: number;
    member_id: number;
}

export interface Event {
    id: number;
    name: string;
    date: string; // ISO date string
    location: string | null;
}

// User context types
export type UserRole = "member" | "institution" | "eb" | "ib" | "admin";

export interface User {
    id: string;
    name: string;
    email: string;
    role: UserRole;
    institutionId?: number; // If an institution user, link to their institution
}