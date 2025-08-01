// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { userCheckAuthStatus, userLogout } from '../client/index';

interface User {
    email: string;
    name: string;
    isadmin: boolean;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (redirectUrl?: string) => void;
    logout: () => Promise<void>;
    checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const checkAuth = async () => {
        try {
            setIsLoading(true);
            const response = await userCheckAuthStatus();

            if (response.data) {
                setUser({
                    email: response.data.email,
                    name: response.data.name,
                    isadmin: response.data.isAdmin
                });
            } else {
                setUser(null);
            }
        } catch (error) {
            console.log('Not authenticated');
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    const login = (redirectUrl: string = '/') => {
        // Redirect to FastAPI login endpoint
        const loginUrl = new URL('/api/v1/user/login', window.location.origin);
        loginUrl.searchParams.set('redirect_url', redirectUrl);
        window.location.href = loginUrl.toString();
    };

    const logout = async () => {
        try {
            await userLogout();
            setUser(null);
            // Redirect to home page or login page after logout
            window.location.href = '/';
        } catch (error) {
            console.error('Logout error:', error);
            // Even if logout fails on server, clear local state
        } finally {
            setUser(null);
            // Redirect to a public page like the login page or home page
            window.location.href = '/login';
            // Or if you have a homepage, you can redirect there: window.location.href = '/';
        }
    };

    useEffect(() => {
        checkAuth();
    }, []);

    const value: AuthContextType = {
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        checkAuth
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};