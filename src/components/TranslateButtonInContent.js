import React from 'react'
import { useTranslator } from '@site/src/hooks/useTranslator';

export default function TranslateButtonInContent() {
  const { changeLanguage, language } = useTranslator();
  return (
    <button
      onClick={() => changeLanguage(language === 'ur' ? 'en' : 'ur')}
      className="button button--secondary button--sm"
    >
      {language === 'ur' ? 'Switch to English' : 'Translate to Urdu'}
    </button>
  );
}
