import React from 'react';
import Chatbot from '../components/Chatbot';
import ContextMenu from '../components/ContextMenu';

function Root({ children }) {
  return (
    <>
      {children}
      <Chatbot />
      <ContextMenu />
    </>
  );
}

export default Root;

