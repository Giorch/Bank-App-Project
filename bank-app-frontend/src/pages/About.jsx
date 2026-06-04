import "./About.css";

function About() {
    return (
        <div className="page-container">
            <div className="about-section">
                <h2>About Bank App</h2>
                <p>
                    Bank App is a modern banking application designed to provide seamless customer and account management. 
                    Built with React and powered by a robust backend API, our application ensures security, reliability, and ease of use.
                </p>
                <h3>Key Features</h3>
                <ul className="features-list">
                    <li>✓ Complete customer management system</li>
                    <li>✓ Multiple account handling</li>
                    <li>✓ Real-time data synchronization</li>
                    <li>✓ User-friendly interface</li>
                    <li>✓ Secure data handling</li>
                    <li>✓ RESTful API integration</li>
                </ul>
                <h3>Technology Stack</h3>
                <div className="tech-stack">
                    <div className="tech-item">Frontend: React, Vite, CSS3</div>
                    <div className="tech-item">Backend: Python, Flask</div>
                    <div className="tech-item">Database: MongoDB</div>
                </div>
            </div>
        </div>
    );
}

export default About;
