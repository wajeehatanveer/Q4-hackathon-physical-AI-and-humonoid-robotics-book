import React from 'react';
import { useChatStore } from '../../store/useChatStore';
import styles from './styles.module.css';

interface Props {
  pageContent: string;
}

const AskAIButton = ({ pageContent }: Props) => {
  const { openChat } = useChatStore();

  const handleAsk = () => {
    openChat(pageContent);
  };

  return (
    <div className={styles.askButtonContainer}>
      <button className={styles.askButton} onClick={handleAsk}>
        Ask AI about this page
      </button>
    </div>
  );
};

export default AskAIButton;
