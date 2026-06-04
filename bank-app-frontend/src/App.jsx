import { useState } from "react";
import Header from "./components/Header";
import Data from "./pages/Data";
import Home from "./pages/Home";
import About from "./pages/About";
import Contact from "./pages/Contact";
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
            case "about":
                return <About />;
            case "contact":
                return <Contact />;
            case "data":
                return <Data />;
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
