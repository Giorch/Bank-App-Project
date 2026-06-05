import { useState, useEffect } from "react";
import {
    getAllAccounts,
    getAccountById,
    createAccount,
    updateAccount,
    deleteAccount,
    getAllCustomers
} from "../api/DataService";
import "./Account.css";

function Account() {
    const [accounts, setAccounts] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [error, setError] = useState(null);

    const [newAccount, setNewAccount] = useState({ accountType: "", balance: "" })
    const [selectedCustomerId, setSelectedCustomerId] = useState("");
    const [editAccount, setEditAccount] = useState(null);

    useEffect(() => {
        fetchAccounts();
        fetchCustomers();
    }, []);

    const fetchAccounts = async () => {
        try {
            const response = await getAllAccounts();
            setAccounts(response.data);
        } catch (err) {
            setError("Failed to load accounts");
        }
    };

    const fetchCustomers = async () => {
        try {
            const response = await getAllCustomers();
            setCustomers(response.data);
        } catch (err) {
            setError("Failed to load customers");
        }
    };

    const handleCreate = async () => {
        if (!selectedCustomerId) {
            setError("Please select a customer");
            return;
        }

        if (!newAccount.accountType) {
            setError("Please select an account type");
            return;
        }

        try {
            await createAccount(selectedCustomerId, { ...newAccount, balance: parseFloat(newAccount.balance) });
            setNewAccount({ accountType: "", balance: "" });
            setSelectedCustomerId("");
            fetchAccounts();
        } catch (err) {
            setError("Failed to create account");
        }
    };

    const handleUpdate = async () => {
        try {
            await updateAccount(editAccount.accountId, editAccount);
            setEditAccount(null);
            fetchAccounts();
        } catch (err) {
            setError("Failed to update account");
        }
    };

    const handleDelete = async (id) => {
        try {
            await deleteAccount(id);
            fetchAccounts();
        } catch (err) {
            setError("Failed to delete account");
        }
    };

    return (
        <div className="account-container">
            <h2>Accounts</h2>

            {error && <p className="error">{error}</p>}

            <div className="form-section">
                <h3>Add Account</h3>
                <select
                    value={selectedCustomerId}
                    onChange={(e) => setSelectedCustomerId(e.target.value)}
                >
                    <option value="">Select a customer</option>
                    {customers.map((customer) => (
                        <option key={customer.id} value={customer.id}>
                            {customer.name}
                        </option>
                    ))}
                </select>
                <select
                    value={newAccount.accountType}
                    onChange={(e) =>
                        setNewAccount({
                            ...newAccount,
                            accountType: e.target.value
                        })
                    }
                >
                    <option value="">Select Account Type</option>
                    <option value="Checking">Checking</option>
                    <option value="Savings">Savings</option>
                </select>
                <input
                    placeholder="Balance"
                    type="number"
                    value={newAccount.balance}
                    onChange={(e) => setNewAccount({ ...newAccount, balance: e.target.value })}
                />
                <button onClick={handleCreate}>Add</button>
            </div>

            {editAccount && (
                <div className="form-section">
                    <h3>Edit Account</h3>
                    <input
                        placeholder="Account Type"
                        value={editAccount.accountType}
                        onChange={(e) => setEditAccount({ ...editAccount, accountType: e.target.value })}
                    />
                    <input
                        placeholder="Balance"
                        type="number"
                        value={editAccount.balance}
                        onChange={(e) => setEditAccount({ ...editAccount, balance: e.target.value })}
                    />
                    <button onClick={handleUpdate}>Save</button>
                    <button onClick={() => setEditAccount(null)}>Cancel</button>
                </div>
            )}

            <table className="account-table">
                <thead>
                    <tr>
                        <th>Account ID</th>
                        <th>Account Type</th>
                        <th>Balance</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {accounts.map((account) => (
                        <tr key={account.accountId}>
                            <td>{account.accountId}</td>
                            <td>{account.accountType}</td>
                            <td>${parseFloat(account.balance).toFixed(2)}</td>
                            <td>
                                <button onClick={() => setEditAccount(account)}>Edit</button>
                                <button onClick={() => handleDelete(account.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Account;
