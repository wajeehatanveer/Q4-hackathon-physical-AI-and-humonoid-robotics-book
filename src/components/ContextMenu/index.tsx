import React, { useState, useEffect, useCallback } from 'react';
import styles from './styles.module.css';
import { useChatStore } from '../../store/useChatStore';

const ContextMenu = () => {
    const [contextMenu, setContextMenu] = useState<{ x: number, y: number, text: string } | null>(null);
    const { openChat } = useChatStore();

    const handleMouseUp = useCallback(() => {
        const selectedText = window.getSelection().toString().trim();
        if (selectedText) {
            const range = window.getSelection().getRangeAt(0);
            const rect = range.getBoundingClientRect();
            setContextMenu({
                x: rect.left + window.scrollX,
                y: rect.bottom + window.scrollY + 5,
                text: selectedText,
            });
        } else {
            setContextMenu(null);
        }
    }, []);

    const handleAskAI = () => {
        if (contextMenu) {
            openChat(contextMenu.text);
            setContextMenu(null);
        }
    };
    
    // Close context menu on click outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            // A bit of a hack to not hide the menu when the button itself is clicked
            if (contextMenu && !(event.target as HTMLElement).closest(`.${styles.contextMenu}`)) {
                setContextMenu(null);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        document.addEventListener('mouseup', handleMouseUp);
        
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, [contextMenu, handleMouseUp]);


    if (!contextMenu) {
        return null;
    }

    return (
        <div className={styles.contextMenu} style={{ top: contextMenu.y, left: contextMenu.x }}>
            <button onClick={handleAskAI}>
                Ask AI about this text
            </button>
        </div>
    );
};

export default ContextMenu;
