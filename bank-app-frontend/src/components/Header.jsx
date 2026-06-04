import { useState } from "react";
import "./Header.css";

function Header({ onNavigate, currentPage }) {
    const navItems = [
        { id: "home", label: "Home" },
        { id: "about", label: "About" },
        { id: "contact", label: "Contact" },
        { id: "data", label: "Data" }
    ];

    return (
        <header className="app-header">
            <div className="header-container">
                <div className="header-brand">
                    <h1>🏦 Bank App</h1>
                </div>
                <nav className="header-nav">
                    {navItems.map((item) => (
                        <button
                            key={item.id}
                            className={`nav-button ${currentPage === item.id ? "active" : ""}`}
                            onClick={() => onNavigate(item.id)}
                        >
                            {item.label}
                        </button>
                    ))}
                </nav>
            </div>
        </header>
    );
}

export default Header;
