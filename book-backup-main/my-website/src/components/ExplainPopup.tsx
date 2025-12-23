import React, { useState, useEffect, useRef } from 'react';

interface ExplainPopupProps {
  selectedText: string;
  onSelectExplain: (text: string) => void;
  isOpen: boolean;
  position: { top: number; left: number } | null;
}

const ExplainPopup: React.FC<ExplainPopupProps> = ({
  selectedText,
  onSelectExplain,
  isOpen,
  position
}) => {
  const popupRef = useRef<HTMLDivElement>(null);

  // Handle clicks outside the popup or elsewhere on the page to close it
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
        // Close the popup if clicking outside of it
        onSelectExplain(''); // Pass empty string to close popup only
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onSelectExplain]);

  if (!isOpen || !position || !selectedText) {
    return null;
  }

  return (
    <div
      ref={popupRef}
      className="explain-popup"
      style={{
        position: 'fixed',
        top: position.top - 40,
        left: position.left,
        zIndex: 1002,
        backgroundColor: '#4f46e5',
        color: 'white',
        borderRadius: '6px',
        padding: '6px 10px',
        fontSize: '14px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        transform: 'translateY(-10px)',
        opacity: 0,
        animation: 'fadeInSlideUp 0.2s forwards',
      }}
    >
      <style>{`
        @keyframes fadeInSlideUp {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
      <span
        onClick={(e) => {
          e.stopPropagation(); // Prevent the click from bubbling up to the document
          onSelectExplain(selectedText);
        }}
        style={{ cursor: 'pointer' }}
      >
        Explain
      </span>
    </div>
  );
};

export default ExplainPopup;