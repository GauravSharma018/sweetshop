import { useState } from "react";
import api from "../api/api";

export default function Register({ goToLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async () => {
    try {
      await api.post("/auth/register", {
        username,
        password,
      });
      goToLogin();
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Create Account ✨</h2>

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

        <p style={{ marginTop: 10 }}>
          Already have an account?{" "}
          <button className="secondary" onClick={goToLogin}>
            Login
          </button>
        </p>
      </div>
    </div>
  );
}
