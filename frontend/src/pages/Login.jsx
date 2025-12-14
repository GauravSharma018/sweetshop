import { useState } from "react";
import api from "../api/api";

export default function Login({ onLogin, goToRegister }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await api.post("/auth/login", {
        username,
        password,
      });

      localStorage.setItem("token", res.data.access_token);
      onLogin();
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Welcome Back 👋</h2>

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

        <button onClick={handleLogin}>Login</button>

        <p style={{ marginTop: 10 }}>
          New user?{" "}
          <button className="secondary" onClick={goToRegister}>
            Register
          </button>
        </p>
      </div>
    </div>
  );
}
