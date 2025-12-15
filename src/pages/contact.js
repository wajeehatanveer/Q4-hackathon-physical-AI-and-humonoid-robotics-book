import React from 'react';
import Layout from '@theme/Layout';

function Contact() {
  return (
    <Layout title="Contact Us" description="Contact the authors of the Physical AI & Humanoid Robotics Book.">
      <main className="container margin-vert--lg">
        <h1>Contact Us</h1>
        <p>
          We welcome your feedback, questions, and suggestions.
          Please reach out to us using the form below or via email.
        </p>
        <form>
          <div className="margin-bottom--md">
            <input type="text" placeholder="Your Name" className="input input--lg" required />
          </div>
          <div className="margin-bottom--md">
            <input type="email" placeholder="Your Email" className="input input--lg" required />
          </div>
          <div className="margin-bottom--md">
            <textarea placeholder="Your Message" className="input input--lg" rows="5" required></textarea>
          </div>
          <button type="submit" className="button button--primary button--lg">Send Message</button>
        </form>
      </main>
    </Layout>
  );
}

export default Contact;