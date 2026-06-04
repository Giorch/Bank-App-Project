import { useState } from "react";
import Header from "./components/Header";
import Customer from "./pages/Customer";
import Account from "./pages/Account";
import Home from "./pages/Home";
import "./App.css";

function App() {
    const [currentPage, setCurrentPage] = useState("home");

    const handleNavigate = (page) => {
        setCurrentPage(page);
    };

    const renderPage = () => {
        switch (currentPage) {
            case "home":
                return <Home />;
            case "customer":
                return <Customer />;
            case "account":
                return <Account />;
            default:
                return <Home />;
        }
    };

    return (
        <div>
            <Header onNavigate={handleNavigate} currentPage={currentPage} />
            <main className="main-content">
                {renderPage()}
            </main>
        </div>
    );
}

export default App;
