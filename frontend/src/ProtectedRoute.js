import { AuthProvider } from './AuthContext';
import LoginForm from './LoginForm';
import AdminPanel from './AdminPanel';
import NLQueryForm from './NLQueryForm';
import ProtectedRoute from './ProtectedRoute';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/admin" element={
            <ProtectedRoute requiredRole="admin">
              <AdminPanel />
            </ProtectedRoute>
          } />
          <Route path="/nl-query" element={
            <ProtectedRoute>
              <NLQueryForm />
            </ProtectedRoute>
          } />
          {/* Add more routes as needed */}
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App; 