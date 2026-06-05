import React, { useState, useEffect } from "react";
import {
    getAllCustomers,
    getPremiumCustomers,
    createCustomer,
    updateCustomer,
    deleteCustomer
} from "../api/DataService";
import "./Customer.css";

function Customer() {
    const [customers, setCustomers] = useState([]);
    const [premiumCustomers, setPremiumCustomers] = useState([]);
    const [error, setError] = useState(null);

    const [newCustomer, setNewCustomer] = useState({name:"", email: ""})
    const [editCustomer, setEditCustomer] = useState(null);
    const [showPremium, setShowPremium] = useState(false); 
     const [expandedCustomerId, setExpandedCustomerId] = useState(null);

    useEffect(() => {
        fetchCustomers();
        fetchPremiumCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await getAllCustomers();
            setCustomers(response.data);
        } catch (err) {
            setError("Failed to load customers");
        }
    };

    const fetchPremiumCustomers = async () => {
        try {
            const response = await getPremiumCustomers();
            setPremiumCustomers(response.data);
        } catch (err) {
            console.log("No premium customers or error loading them");
        }
    };

    const handleCreate = async () => {

        if (!newCustomer.name.trim()) {
        setError("Name is required");
        return;
        }

        if (!newCustomer.email.trim()) {
            setError("Email is required");
            return;
        }
        try {
            await createCustomer({ ...newCustomer, accounts: [] });
            setNewCustomer({ name: "", email: "" });
            fetchCustomers();
            fetchPremiumCustomers();
        } catch (err) {
            setError("Failed to create customer");
        }
    };

    const handleUpdate = async () => {
        try {
            await updateCustomer(editCustomer.id, editCustomer);
            setEditCustomer(null);
            fetchCustomers();
            fetchPremiumCustomers();
        } catch (err) {
            setError("Failed to update customer");
        }
    };

    const handleDelete = async (id) => {
        try {
            await deleteCustomer(id);
            fetchCustomers();
            fetchPremiumCustomers();
        } catch (err) {
            setError("Failed to delete customer");
        }
    };

    const CustomerTable = ({ data}) =>(
    
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
                    {data.map((c) => (
                        <React.Fragment key={c.id}>
                        <tr>
                            <td>{c.id}</td>
                            <td>{c.name}</td>
                            <td>{c.email}</td>
                            <td>
                                <button onClick={() => setExpandedCustomerId(expandedCustomerId === c.id ? null : c.id)}>
                                        {expandedCustomerId === c.id ? "Hide Accounts" : "View Accounts"}
                                    </button>
                                <button onClick={() => setEditCustomer(c)}>Edit</button>
                                <button onClick={() => handleDelete(c.id)}>Delete</button>
                            </td>
                        </tr>
                            {expandedCustomerId === c.id && c.accounts && c.accounts.length > 0 && (
                                <tr>
                                    <td colSpan="4">
                                        <table className="accounts-table">
                                            <thead>
                                                <tr>
                                                    <th>Account ID</th>
                                                    <th>Type</th>
                                                    <th>Balance</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {c.accounts.map((a) => (
                                                    <tr key={a.accountId}>
                                                        <td>{a.accountId}</td>
                                                        <td>{a.accountType}</td>
                                                        <td>${a.balance.toLocaleString()}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            )}
                        </React.Fragment>
                    ))}
                </tbody>
            </table>
    );
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

              <div className="view-toggle">
                <button onClick={() => setShowPremium(false)} className={!showPremium ? "active" : ""}>
                    All Customers
                </button>
                <button onClick={() => setShowPremium(true)} className={showPremium ? "active" : ""}>
                    Premium Customers ({premiumCustomers.length})
                </button>
               </div>

               <h2>{showPremium ? "Premium Customers" : "All Customers"}</h2>
                {showPremium ? (
                premiumCustomers.length > 0 ? (
                    <CustomerTable data={premiumCustomers} />
                ) : (
                    <p>No premium customers</p>
                )
                 ) : (
                <CustomerTable data={customers} />
                )}

        </div>
    );
}

export default Customer;
