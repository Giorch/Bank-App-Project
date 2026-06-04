import { useState } from "react";
import "./Contact.css";

function Contact() {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        subject: "",
        message: ""
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Form submitted:", formData);
        alert("Thank you for contacting us! We'll get back to you soon.");
        setFormData({ name: "", email: "", subject: "", message: "" });
    };

    return (
        <div className="page-container">
            <div className="contact-section">
                <h2>Contact Us</h2>
                <p>Get in touch with our team. We'd love to hear from you!</p>
                
                <div className="contact-wrapper">
                    <div className="contact-info">
                        <h3>Contact Information</h3>
                        <div className="info-item">
                            <h4>📧 Email</h4>
                            <p>support@bankapp.com</p>
                        </div>
                        <div className="info-item">
                            <h4>📞 Phone</h4>
                            <p>+1 (555) 123-4567</p>
                        </div>
                        <div className="info-item">
                            <h4>📍 Address</h4>
                            <p>123 Banking Street<br />Finance City, FC 12345</p>
                        </div>
                        <div className="info-item">
                            <h4>⏰ Hours</h4>
                            <p>Monday - Friday: 9AM - 6PM<br />Saturday - Sunday: Closed</p>
                        </div>
                    </div>

                    <form className="contact-form" onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="name">Name</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="Your name"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="your@email.com"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="subject">Subject</label>
                            <input
                                type="text"
                                id="subject"
                                name="subject"
                                value={formData.subject}
                                onChange={handleChange}
                                placeholder="Message subject"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="message">Message</label>
                            <textarea
                                id="message"
                                name="message"
                                value={formData.message}
                                onChange={handleChange}
                                placeholder="Your message..."
                                rows="6"
                                required
                            ></textarea>
                        </div>
                        <button type="submit" className="submit-btn">Send Message</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Contact;
