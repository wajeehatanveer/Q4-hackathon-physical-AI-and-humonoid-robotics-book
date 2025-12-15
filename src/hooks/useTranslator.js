import { useState, useContext, createContext, useEffect } from 'react';

// Sample Urdu translations (in a real app, this would be loaded from a file or API)
const urduTranslations = {
  "hello": "ہیلو",
  "welcome": "خوش آمدید",
  "this is a chapter": "یہ ایک باب ہے",
  "translate content": "مواد کا ترجمہ کریں"
};

// Create a Context for the translator
const TranslatorContext = createContext(null);

// Custom hook to provide translation state and functions
export function useTranslator() {
  const context = useContext(TranslatorContext);
  if (!context) {
    throw new Error('useTranslator must be used within a TranslatorProvider');
  }
  return context;
}

// Translator Provider component
export function TranslatorProvider({ children }) {
  const [language, setLanguage] = useState('en'); // Default language is English
  const [currentTranslations, setCurrentTranslations] = useState({});

  useEffect(() => {
    if (language === 'ur') {
      setCurrentTranslations(urduTranslations);
    } else {
      setCurrentTranslations({}); // Clear translations if not Urdu
    }
  }, [language]);

  // Function to change language
  const changeLanguage = (newLang) => {
    setLanguage(newLang);
  };

  // Function to translate a key
  const translate = (key, defaultText = key) => {
    return currentTranslations[key] || defaultText;
  };

  const value = {
    language,
    changeLanguage,
    translate,
  };

  return (
    <TranslatorContext.Provider value={value}>
      {children}
    </TranslatorContext.Provider>
  );
}
