import "./Home.css";

function Home({ onNavigate }) {
    return (
        <div className="page-container">
            <div className="hero-section">
                <h2>Welcome to Bank App</h2>
                <p>Manage your banking needs with ease and security</p>
                <div className="features">
                    <div className="feature-card" onClick={() => onNavigate("customer")}>
                        <h3>👥 Customers</h3>
                        <p>Customer management system</p>
                    </div>
                    <div className="feature-card" onClick={() => onNavigate("account")}>
                        <h3>💳 Accounts</h3>
                        <p>Manage multiple accounts</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;
