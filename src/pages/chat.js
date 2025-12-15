import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';
import styles from './chat.module.css';

const ChatPage = () => {
    return (
        <Layout title="Chat">
            <div className={styles.chatPageContainer}>
                <div className={styles.embeddedChat}>
                   {/* For a full-page experience, the Chatbot component would be
                       styled differently here, but for now we reuse it as is. */}
                   <Chatbot />
                </div>
            </div>
        </Layout>
    );
};

export default ChatPage;
