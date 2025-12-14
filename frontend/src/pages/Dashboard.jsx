import { useEffect, useState } from "react";
import api from "../api/api";

export default function Dashboard({ onLogout }) {
  const [sweets, setSweets] = useState([]);
  const [search, setSearch] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    loadSweets();
    checkAdmin();
  }, []);

  const loadSweets = async () => {
    const res = await api.get("/sweets");
    setSweets(res.data);
  };

  const checkAdmin = async () => {
    try {
      const res = await api.get("/auth/me");
      setIsAdmin(res.data.is_admin);
    } catch {}
  };

  const buySweet = async (id) => {
    await api.post(`/sweets/${id}/purchase`);
    loadSweets();
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>🍬 Sweet Shop</h1>
        <button className="danger" onClick={onLogout}>
          Logout
        </button>
      </div>

      <input
        className="search"
        placeholder="Search sweets..."
        onChange={e => setSearch(e.target.value)}
      />

      {isAdmin && (
        <div className="admin-panel">
          <h3>Admin Controls</h3>
          <p>Add / Update / Restock sweets from backend (UI optional)</p>
        </div>
      )}

      <div className="grid">
        {sweets
          .filter(s =>
            s.name.toLowerCase().includes(search.toLowerCase())
          )
          .map(sweet => (
            <div className="card" key={sweet.id}>
              <h3>{sweet.name}</h3>
              <p>Category: {sweet.category}</p>
              <p>Price: ₹{sweet.price}</p>
              <p>Stock: {sweet.quantity}</p>

              <button
                disabled={sweet.quantity === 0}
                onClick={() => buySweet(sweet.id)}
              >
                {sweet.quantity === 0 ? "Out of Stock" : "Buy"}
              </button>
            </div>
          ))}
      </div>
    </div>
  );
}
