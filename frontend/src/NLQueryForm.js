import React, { useState } from "react";
import { useAuth } from "./AuthContext";

export default function NLQueryForm() {
  const { token } = useAuth();
  const [instruction, setInstruction] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/agent/nl_query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ instruction }),
      });
      const data = await response.json();
      if (!response.ok || data.success === false) {
        setError(data.message || "Query failed");
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Natural Language Query</h2>
      <form onSubmit={handleSubmit}>
        <input
          value={instruction}
          onChange={e => setInstruction(e.target.value)}
          placeholder="e.g. Show all employees in HR"
          style={{ width: "60%" }}
          required
        />
        <button type="submit" disabled={loading} style={{ marginLeft: 8 }}>
          {loading ? "Running..." : "Run"}
        </button>
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 16 }}>
          <div><b>SQL:</b> <code>{result.sql}</code></div>
          <div><b>Message:</b> {result.message}</div>
          <div><b>Data:</b>
            <pre style={{ background: "#f4f4f4", padding: 8 }}>{JSON.stringify(result.data, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
} 