import { useState, useEffect } from "react";
import {
    getAllCustomers,
    createCustomer,
    updateCustomer,
    deleteCustomer
} from "../api/DataService";
import "./Data.css";

function Data() {
    const [customers, setCustomers] = useState([]);
    const [error, setError] = useState(null);

    const [newCustomer, setNewCustomer] = useState({name:"", email: ""})
    const [editCustomer, setEditCustomer] = useState(null);

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await getAllCustomers();
            setCustomers(response.data);
        } catch (err) {
            setError("Failed to load customers");
        }
    };

    const handleCreate = async () => {
        try {
            await createCustomer({ ...newCustomer, accounts: [] });
            setNewCustomer({ name: "", email: "" });
            fetchCustomers();
        } catch (err) {
            setError("Failed to create customer");
        }
    };

    const handleUpdate = async () => {
        try {
            await updateCustomer(editCustomer.id, editCustomer);
            setEditCustomer(null);
            fetchCustomers();
        } catch (err) {
            setError("Failed to update customer");
        }
    };

    const handleDelete = async (id) => {
        try {
            await deleteCustomer(id);
            fetchCustomers();
        } catch (err) {
            setError("Failed to delete customer");
        }
    };

    return (
        <div className="data-container">
            <h2>Customers</h2>

            {error && <p className="error">{error}</p>}

            <div className="form-section">
                <h3>Add Customer</h3>
                <input
                    placeholder="Name"
                    value={newCustomer.name}
                    onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })}
                />
                <input
                    placeholder="Email"
                    value={newCustomer.email}
                    onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })}
                />
                <button onClick={handleCreate}>Add</button>
            </div>

              {editCustomer && (
                <div className="form-section">
                    <h3>Edit Customer</h3>
                    <input
                        value={editCustomer.name}
                        onChange={(e) => setEditCustomer({ ...editCustomer, name: e.target.value })}
                    />
                    <input
                        value={editCustomer.email}
                        onChange={(e) => setEditCustomer({ ...editCustomer, email: e.target.value })}
                    />
                    <button onClick={handleUpdate}>Save</button>
                    <button onClick={() => setEditCustomer(null)}>Cancel</button>
                </div>
            )}

             <table className="customer-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {customers.map((c) => (
                        <tr key={c.id}>
                            <td>{c.id}</td>
                            <td>{c.name}</td>
                            <td>{c.email}</td>
                            <td>
                                <button onClick={() => setEditCustomer(c)}>Edit</button>
                                <button onClick={() => handleDelete(c.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Data;

