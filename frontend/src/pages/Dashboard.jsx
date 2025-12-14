import { useEffect, useState } from "react";
import api from "../api/api";
import { getUserFromToken } from "../utils/auth";

export default function Dashboard({ onLogout }) {
  const [sweets, setSweets] = useState([]);
  const [search, setSearch] = useState("");
  const [showAdmin, setShowAdmin] = useState(false);

  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
  });

  const user = getUserFromToken();
  const isAdmin = user?.is_admin;

  const loadSweets = async () => {
    const res = await api.get("/sweets");
    setSweets(res.data);
  };

  useEffect(() => {
    loadSweets();
  }, []);

  const purchaseSweet = async (id) => {
    await api.post(`/sweets/${id}/purchase`);
    loadSweets();
  };

  const addSweet = async () => {
    await api.post("/sweets", {
      ...form,
      price: Number(form.price),
      quantity: Number(form.quantity),
    });
    setForm({ name: "", category: "", price: "", quantity: "" });
    loadSweets();
  };

  const restockSweet = async (id) => {
    const qty = prompt("Enter restock quantity:");
    if (!qty) return;
    await api.post(`/sweets/${id}/restock`, { quantity: Number(qty) });
    loadSweets();
  };

  const deleteSweet = async (id) => {
    if (!confirm("Delete this sweet?")) return;
    await api.delete(`/sweets/${id}`);
    loadSweets();
  };

  const filtered = sweets.filter(
    s =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h2>🍬 Sweet Shop Management</h2>
        <div>
          {isAdmin && (
            <button className="secondary" onClick={() => setShowAdmin(!showAdmin)}>
              Admin Panel
            </button>
          )}
          <button className="secondary" onClick={onLogout}>Logout</button>
        </div>
      </header>

      {showAdmin && isAdmin && (
        <div className="admin-panel">
          <h3>Add New Sweet</h3>
          <input placeholder="Name" value={form.name}
            onChange={e => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Category" value={form.category}
            onChange={e => setForm({ ...form, category: e.target.value })} />
          <input placeholder="Price" value={form.price}
            onChange={e => setForm({ ...form, price: e.target.value })} />
          <input placeholder="Quantity" value={form.quantity}
            onChange={e => setForm({ ...form, quantity: e.target.value })} />
          <button onClick={addSweet}>Add Sweet</button>
        </div>
      )}

      <input
        className="search"
        placeholder="Search by name or category..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div className="grid">
        {filtered.map(sweet => (
          <div className="card" key={sweet.id}>
            <h3>{sweet.name}</h3>
            <p><b>Category:</b> {sweet.category}</p>
            <p><b>Price:</b> ₹{sweet.price}</p>
            <p><b>Stock:</b> {sweet.quantity}</p>

            <button
              disabled={sweet.quantity === 0}
              onClick={() => purchaseSweet(sweet.id)}
            >
              {sweet.quantity === 0 ? "Out of Stock" : "Buy"}
            </button>

            {isAdmin && (
              <>
                <button onClick={() => restockSweet(sweet.id)}>Restock</button>
                <button className="danger" onClick={() => deleteSweet(sweet.id)}>
                  Delete
                </button>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
