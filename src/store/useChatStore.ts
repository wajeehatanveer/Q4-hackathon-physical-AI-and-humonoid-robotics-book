import { create } from 'zustand';

interface ChatState {
  isOpen: boolean;
  selectedText: string | null;
  openChat: (text?: string) => void;
  closeChat: () => void;
  setSelectedText: (text: string) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  isOpen: false,
  selectedText: null,
  openChat: (text) => set({ isOpen: true, selectedText: text || null }),
  closeChat: () => set({ isOpen: false, selectedText: null }),
  setSelectedText: (text) => set({ selectedText: text }),
}));
