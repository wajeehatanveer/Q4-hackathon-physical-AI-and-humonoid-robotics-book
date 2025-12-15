import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';
import { useChatStore } from '../../store/useChatStore';

const Chatbot = () => {
    const { isOpen, selectedText, openChat, closeChat } = useChatStore();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false); // New loading state
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (isOpen && selectedText) {
            inputRef.current?.focus();
        }
        if(isOpen) {
            setMessages([{ role: 'bot', content: "Hello! How can I help you with the Physical AI book?" }]);
        }
    }, [isOpen, selectedText]);

    const handleSend = async () => {
        if (input.trim() === '') return;

        const newMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, newMessage]);
        setInput('');
        setIsLoading(true); // Show loading indicator

        try {
            const response = await fetch('http://localhost:8000/chat', { // Adjust for production
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    query: input, 
                    selected_text: selectedText 
                })
            });

            if (!response.ok) {
                throw new Error('Failed to get response from the chatbot.');
            }

            const data = await response.json();
            const botMessage = { role: 'bot', content: data.answer, sources: data.sources };
            setMessages(prev => [...prev, botMessage]);

        } catch (error) {
            console.error("Chat error:", error);
            const errorMessage = { role: 'bot', content: 'Sorry, something went wrong. Please try again.' };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false); // Hide loading indicator
        }
    };

    return (
        <div>
            <button className={styles.floatingButton} onClick={() => openChat()}>
                🤖
            </button>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader}>
                        <h3>Humanoid Assistant</h3>
                        <button onClick={closeChat}>&times;</button>
                    </div>
                    <div className={styles.chatMessages}>
                         {selectedText && (
                            <div className={`${styles.message} ${styles.context}`}>
                                <p><strong>Context:</strong> "{selectedText}"</p>
                            </div>
                        )}
                        {messages.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.role]}`}>
                                <p>{msg.content}</p>
                                {msg.sources && (
                                    <div className={styles.sources}>
                                        <strong>Sources:</strong>
                                        <ul>
                                            {msg.sources.map((source, i) => <li key={i}>{source}</li>)}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={`${styles.message} ${styles.bot}`}>
                                <div className={styles.typingIndicator}>
                                    <span>.</span>
                                    <span>.</span>
                                    <span>.</span>
                                </div>
                            </div>
                        )}
                    </div>
                    <div className={styles.chatInput}>
                        <input
                            ref={inputRef}
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask a question..."
                        />
                        <button onClick={handleSend}>Send</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
