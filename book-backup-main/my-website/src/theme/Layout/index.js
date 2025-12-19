import React, { useState, useEffect } from 'react';
import Layout from '@theme-original/Layout';
import Chatbot from '../../components/Chatbot';

export default function LayoutWrapper(props) {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleMouseUp = () => {
      const selection = window.getSelection();
      const text = selection ? selection.toString().trim() : '';
      if (text.length > 0 && text.length < 500) { // Limit selection length to avoid huge contexts
        setSelectedText(text);
      } else {
        setSelectedText('');
      }
    };

    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  return (
    <>
      <Layout {...props} />
      <Chatbot initialSelectedText={selectedText} />
    </>
  );
}
