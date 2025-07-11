import { useState } from 'react';
import './App.css';
import reactLogo from './assets/react.svg';

export default function App() {
  const [instruction, setInstruction] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('token') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [loginError, setLoginError] = useState(null);
  const [signupError, setSignupError] = useState(null);
  const [isSignup, setIsSignup] = useState(false);
  const [currentUser, setCurrentUser] = useState(() => localStorage.getItem('username') || '');

  async function handleLogin(e) {
    e.preventDefault();
    setLoginError(null);
    try {
      const body = new URLSearchParams({ username, password });
      console.log('Login request body:', body.toString());
      const response = await fetch('/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      });
      let data = {};
      let rawText = '';
      try {
        rawText = await response.text();
        data = JSON.parse(rawText);
      } catch {
        setLoginError(`Login failed: Server did not return JSON. Status: ${response.status}. Raw response: ${rawText}`);
        console.error('Login failed: Non-JSON response', response.status, rawText);
        return;
      }
      console.log('Login response:', response.status, data);
      if (response.ok && data.access_token) {
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        setCurrentUser(username);
        localStorage.setItem('username', username);
        setUsername('');
        setPassword('');
      } else {
        setLoginError(`Login failed: ${data.detail || 'Unknown error'} (Status: ${response.status})`);
        console.error('Login failed:', response.status, data);
      }
    } catch (err) {
      setLoginError('Login failed: ' + err.message);
      console.error('Login error:', err);
    }
  }

  async function handleSignup(e) {
    e.preventDefault();
    setSignupError(null);
    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
      let data = {};
      let rawText = '';
      try {
        rawText = await response.text();
        data = JSON.parse(rawText);
      } catch {
        setSignupError(`Sign up failed: Server did not return JSON. Status: ${response.status}. Raw response: ${rawText}`);
        return;
      }
      if (response.ok && data.username) {
        // Auto-login after signup
        await handleLogin({
          preventDefault: () => {},
          target: { username: { value: username }, password: { value: password } },
        });
      } else {
        setSignupError(`Sign up failed: ${data.detail || 'Unknown error'} (Status: ${response.status})`);
      }
    } catch (err) {
      setSignupError('Sign up failed: ' + err.message);
    }
  }

  function handleLogout() {
    setToken('');
    setCurrentUser('');
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setResult(null);
    setError(null);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch('/agent/nl_query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ instruction }),
      });
      const data = await response.json();
      console.log('Backend response:', data);
      if (!response.ok || data.success === false) {
        setError(data.message || 'Backend error');
      }
      setResult(data);
    } catch (err) {
      setError('Failed to fetch result. ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="card">
        <img src={reactLogo} className="logo react" alt="React logo" />
        <h1>SQL Agent {isSignup ? 'Sign Up' : 'Login'}</h1>
        <div className="toggle-row">
          {isSignup ? 'Already have an account?' : 'New user?'}
          <button
            type="button"
            className="toggle-btn"
            onClick={() => {
              setIsSignup(!isSignup);
              setLoginError(null);
              setSignupError(null);
            }}
          >
            {isSignup ? 'Sign In' : 'Sign Up'}
          </button>
        </div>
        {isSignup ? (
          <form onSubmit={handleSignup} style={{ marginBottom: 24, width: '100%' }}>
            <input
              name="username"
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
            <input
              name="email"
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
            <input
              name="password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Signing up...' : 'Sign Up'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleLogin} style={{ marginBottom: 24, width: '100%' }}>
            <input
              name="username"
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
            <input
              name="password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
        )}
        {loginError && !isSignup && <div style={{ color: 'red', marginBottom: 12, fontWeight: 600, whiteSpace: 'pre-wrap' }}>{loginError}</div>}
        {signupError && isSignup && <div style={{ color: 'red', marginBottom: 12, fontWeight: 600, whiteSpace: 'pre-wrap' }}>{signupError}</div>}
      </div>
    );
  }

  return (
    <div className="card">
      <div className="user-bar">
        <span>👤 {currentUser}</span>
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </div>
      <img src={reactLogo} className="logo react" alt="React logo" />
      <h1>SQL Agent</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: 24, width: '100%' }}>
        <input
          type="text"
          value={instruction}
          onChange={e => setInstruction(e.target.value)}
          placeholder="Enter your natural language query..."
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>
      {error && <div style={{ color: 'red', marginBottom: 12, fontWeight: 600 }}>{error}</div>}
      {result && result.results && Array.isArray(result.results) ? (
        <div style={{ textAlign: 'left', marginTop: 24, width: '100%' }}>
          <h3>Multi-step Results:</h3>
          {result.results.map((r, idx) => (
            <div key={idx} style={{ marginBottom: 24, border: '1px solid #333', borderRadius: 8, padding: 12, background: '#181a20' }}>
              <div style={{ fontWeight: 700, marginBottom: 4 }}>Step {idx + 1}:</div>
              <div style={{ color: '#0f0', fontFamily: 'monospace', marginBottom: 6 }}><b>SQL:</b> {r.sql}</div>
              {r.error ? (
                <div style={{ color: 'red', marginBottom: 6 }}><b>Error:</b> {r.error}</div>
              ) : null}
              <div style={{ color: r.error ? 'red' : '#aaa', marginBottom: 6 }}>{r.message}</div>
              <div>
                <b>Result:</b>
                <pre style={{ background: '#222', color: '#fff', padding: 8, borderRadius: 6, marginTop: 4 }}>{JSON.stringify(r.data, null, 2)}</pre>
              </div>
            </div>
          ))}
        </div>
      ) : result && (
        <div style={{ textAlign: 'left', marginTop: 24, width: '100%' }}>
          <h3>SQL:</h3>
          <pre style={{ background: '#181818', color: '#0f0', padding: 12, borderRadius: 6 }}>{result.sql || 'No SQL generated.'}</pre>
          <h3>Result:</h3>
          <pre style={{ background: '#181818', color: '#fff', padding: 12, borderRadius: 6 }}>{result.data ? JSON.stringify(result.data, null, 2) : 'No result.'}</pre>
          <div style={{ marginTop: 8, color: result.success ? 'green' : 'red' }}>{result.message}</div>
        </div>
      )}
    </div>
  );
} 