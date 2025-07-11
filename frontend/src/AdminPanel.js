import React from "react";
import { useAuth } from "../AuthContext";

export default function AdminPanel() {
  const { user } = useAuth();

  if (!user || user.role !== "admin") {
    return <div>You are not authorized to view this page.</div>;
  }

  return (
    <div>
      <h2>Admin Panel</h2>
      {/* Admin-only features here */}
      <p>Welcome, {user.username}!</p>
    </div>
  );
} 