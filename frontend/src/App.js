import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AuthProvider, useAuth } from "../AuthContext";
import LoginForm from "../LoginForm";
import AdminPanel from "./AdminPanel";
import ProtectedRoute from "../ProtectedRoute";
import NLQueryForm from "../NLQueryForm";

function Home() {
  const { user, logout } = useAuth();
  return (
    <div>
      <h1>Welcome to SQL Agent Frontend</h1>
      {user ? (
        <>
          <p>Logged in as: {user.username} ({user.role})</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <Link to="/login">Login</Link>
      )}
      <nav>
        <ul>
          <li><Link to="/admin">Admin Panel</Link></li>
          <li><Link to="/nl">Natural Language Query</Link></li>
        </ul>
      </nav>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/admin" element={
            <ProtectedRoute requiredRole="admin">
              <AdminPanel />
            </ProtectedRoute>
          } />
          <Route path="/nl" element={<NLQueryForm />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
} 