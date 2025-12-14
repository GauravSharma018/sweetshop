import { useState } from "react";
import api from "../api/api";

export default function Register({ goToLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async () => {
    // Clear previous messages
    setSuccess("");
    setError("");

    try {
      await api.post("/auth/register", {
        username,
        password,
      });

      setSuccess("Registration successful! Please login.");
      setUsername("");
      setPassword("");
    } catch (err) {
      if (err.response?.status === 400) {
        setError(err.response.data.detail || "User already exists");
      } else if (err.response?.status === 422) {
        setError("Invalid input");
      } else {
        setError("Registration failed. Please try again.");
      }
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Register</h2>

        {success && <p style={{ color: "green" }}>{success}</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        <input
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <button onClick={handleRegister}>Register</button>

        <p style={{ marginTop: "10px" }}>
          <button className="secondary" onClick={goToLogin}>
            Back to Login
          </button>
        </p>
      </div>
    </div>
  );
}
