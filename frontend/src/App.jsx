import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("token")
  );
  const [showRegister, setShowRegister] = useState(false);

  const logout = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
  };

  if (!loggedIn) {
    return showRegister ? (
      <Register goToLogin={() => setShowRegister(false)} />
    ) : (
      <Login
        onLogin={() => setLoggedIn(true)}
        goToRegister={() => setShowRegister(true)}
      />
    );
  }

  return <Dashboard onLogout={logout} />;
}
