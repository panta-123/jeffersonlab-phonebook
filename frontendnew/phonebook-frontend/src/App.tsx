import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import MembersPage from './pages/MembersPage'; // Import MembersPage
import InstitutionPage from './pages/InstitutionPage'; // Import MembersPage

import NavBar from './components/NavBar';
import { checkAuthStatus } from './utils/auth'; // Import checkAuthStatus
import type { AuthStatus } from './client/types.gen'; // Import AuthStatus type

const App: React.FC = () => {
  const [authStatus, setAuthStatus] = useState<AuthStatus | null>(null);
  const [loadingAuth, setLoadingAuth] = useState<boolean>(true);

  // Fetch initial authentication status when the app mounts
  useEffect(() => {
    const getInitialAuthStatus = async () => {
      setLoadingAuth(true);
      const status = await checkAuthStatus();
      setAuthStatus(status);
      setLoadingAuth(false);
    };
    getInitialAuthStatus();
  }, []); // Runs only once on component mount

  // A PrivateRoute component to protect routes
  const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    // While auth status is loading, show nothing or a loading spinner
    if (loadingAuth) {
      return (
        <div className="flex items-center justify-center min-h-screen">
          <p className="text-lg text-gray-700">Checking authentication...</p>
        </div>
      );
    }
    // If authenticated, render the children (the protected component)
    // Else, redirect to login, preserving the current location
    return authStatus?.authenticated ? (
      <>{children}</>
    ) : (
      <Navigate to="/login" replace state={{ from: location.pathname }} />
    );
  };

  return (
    <Router>
      {/* NavBar now receives authStatus and loadingAuth as props */}
      <NavBar authStatus={authStatus} loadingAuth={loadingAuth} />
      <main className="flex-grow"> {/* Use flex-grow to push footer down if you add one */}
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/members"
            element={
              <PrivateRoute>
                <MembersPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/institutions"
            element={
              <PrivateRoute>
                <InstitutionPage />
              </PrivateRoute>
            }
          />
          {/* Default route: if authenticated, go to dashboard; otherwise, go to login */}
          <Route
            path="/"
            element={
              loadingAuth ? (
                <div className="flex items-center justify-center min-h-screen">
                  <p className="text-lg text-gray-700">Initializing...</p>
                </div>
              ) : authStatus?.authenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          {/* Add more protected routes here */}
          {/* Example: <Route path="/profile" element={<PrivateRoute><ProfilePage /></PrivateRoute>} /> */}
        </Routes>
      </main>
    </Router>
  );
};

export default App;