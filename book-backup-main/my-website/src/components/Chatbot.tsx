import React, { useState, useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Array<{ source: string; heading?: string }>;
}

interface ChatbotProps {
  initialSelectedText?: string;
}

const Chatbot: React.FC<ChatbotProps> = ({ initialSelectedText }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [isMobile, setIsMobile] = useState(false);

  // Check if mobile device and update state
  useEffect(() => {
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkIsMobile();
    window.addEventListener('resize', checkIsMobile);

    return () => {
      window.removeEventListener('resize', checkIsMobile);
    };
  }, []);

  useEffect(() => {
    if (initialSelectedText) {
      setIsOpen(true);
      setSelectedText(initialSelectedText);
      setInput(initialSelectedText); // Pre-fill input with selected text
    }
  }, [initialSelectedText]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Add text selection functionality
  useEffect(() => {
    const handleTextSelection = () => {
      const selectedText = window.getSelection()?.toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    const handleClick = () => {
      // Clear selected text when clicking elsewhere
      setTimeout(() => {
        const currentSelection = window.getSelection()?.toString().trim();
        if (!currentSelection) {
          setSelectedText('');
        }
      }, 100);
    };

    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('click', handleClick);
    };
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const startNewChat = () => {
    setMessages([]);
    setConversationId(null);
    setInput('');
  };

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Remove authentication requirement since backend doesn't require it
      // Use environment-aware API endpoint
      const isDev = typeof window !== 'undefined'
        ? window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        : false;

      let backendUrl = isDev
        ? 'http://localhost:8000'  // Development
        : window.ENV?.REACT_APP_API_BASE_URL ||
          window.ENV?.NEXT_PUBLIC_API_BASE_URL ||
          (typeof process !== 'undefined' ? (process.env?.REACT_APP_API_BASE_URL || process.env?.NEXT_PUBLIC_API_BASE_URL) : null) ||
          'https://web-production-f3886.up.railway.app'; // Railway backend URL

      // If no backend URL is configured for production, show an error
      if (!isDev && !backendUrl) {
        throw new Error('Backend API URL is not configured for production');
      }

      const response = await fetch(`${backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: input,
          conversation_id: conversationId,
          selected_text: selectedText || initialSelectedText, // Send currently selected text or initial text
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const conversation = await response.json();

      // Update conversation ID
      setConversationId(conversation.id);

      // Set all messages from the response (this includes both user and assistant messages)
      setMessages(conversation.messages);
    } catch (error) {
      console.error('Chatbot API error:', error);
      let errorMessage = 'Sorry, I am having trouble connecting right now. Please try again later.';

      // Provide more specific error message if it's a configuration issue
      if (error instanceof Error && error.message === 'Backend API URL is not configured for production') {
        errorMessage = 'Backend API is not configured. Please contact the site administrator to set up the backend connection.';
      }

      // Remove the user message and add an error message
      setMessages(prev => {
        const messagesWithoutLastUser = prev.filter((_, index) => !(index === prev.length - 1 && prev[index].role === 'user'));
        return [
          ...messagesWithoutLastUser,
          { role: 'assistant', content: errorMessage },
        ];
      });
    } finally {
      setIsLoading(false);
    }
  };

  const askAboutSelection = () => {
    if (selectedText) {
      // Create a more contextual prompt for the selected text
      const prompt = selectedText.length > 100
        ? `Please explain this concept from the documentation: "${selectedText.substring(0, 100)}..."`
        : `What does this mean: "${selectedText}"?`;
      setInput(prompt);
      setTimeout(() => {
        setIsOpen(true);
      }, 100);
    }
  };

  // Add typing indicator animation styles and responsive styles
  const responsiveStyles = `
    .typing-indicator {
      display: inline-block;
    }
    .typing-indicator::after {
      content: '';
      animation: typing 1.4s infinite;
    }
    @keyframes typing {
      0%, 60%, 100% { content: ''; }
      20% { content: '.'; }
      40% { content: '..'; }
      60% { content: '...'; }
    }

    /* Responsive styles */
    @media (max-width: 768px) {
      .chatbot-container {
        width: calc(100% - 40px) !important;
        height: 80vh !important;
        max-height: 600px;
        bottom: 80px !important;
        right: 20px !important;
        left: 20px !important;
        border-radius: 16px !important;
      }

      .chatbot-button {
        width: 50px !important;
        height: 50px !important;
        bottom: 15px !important;
        right: 15px !important;
      }

      .selection-button {
        width: 40px !important;
        height: 40px !important;
        top: 15px !important;
        right: 15px !important;
        font-size: 16px !important;
      }

      .chat-header {
        padding: 12px 15px !important;
      }

      .chat-header-title {
        font-size: 16px !important;
      }

      .chat-messages {
        padding: 12px !important;
      }

      .message-bubble {
        max-width: 90% !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
      }

      .message-role {
        font-size: 11px !important;
      }

      .chat-input-area {
        padding: 12px !important;
      }

      .chat-input {
        padding: 10px 12px !important;
        font-size: 14px !important;
      }

      .send-button {
        padding: 10px 16px !important;
        font-size: 13px !important;
      }

      .welcome-text {
        font-size: 13px !important;
        padding: 15px !important;
      }

      .welcome-title {
        font-size: 15px !important;
        margin-bottom: 6px !important;
      }
    }

    @media (max-width: 480px) {
      .chatbot-container {
        width: calc(100% - 20px) !important;
        height: 85vh !important;
        bottom: 70px !important;
        right: 10px !important;
        left: 10px !important;
      }

      .chatbot-button {
        width: 45px !important;
        height: 45px !important;
        bottom: 10px !important;
        right: 10px !important;
      }

      .selection-button {
        width: 36px !important;
        height: 36px !important;
        top: 10px !important;
        right: 10px !important;
      }

      .message-bubble {
        max-width: 95% !important;
        padding: 9px 12px !important;
      }

      .chat-input {
        padding: 9px 10px !important;
      }

      .send-button {
        padding: 9px 14px !important;
      }
    }
  `;

  return (
    <>
      <style>{responsiveStyles}</style>

      {/* Floating button that appears when text is selected */}
      {selectedText && (
        <button
          onClick={askAboutSelection}
          className="selection-button"
          style={{
            position: 'fixed',
            top: isMobile ? '10px' : '20px',
            right: isMobile ? '10px' : '20px',
            zIndex: 1001,
            backgroundColor: '#10b981',
            color: 'white',
            borderRadius: '24px',
            width: isMobile ? '36px' : '48px',
            height: isMobile ? '36px' : '48px',
            border: 'none',
            cursor: 'pointer',
            fontSize: isMobile ? '16px' : '18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            transition: 'all 0.2s ease',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.05)';
            e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.2)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
          }}
          title="Ask about selected text"
        >
          💬
        </button>
      )}

      <button
        onClick={toggleChat}
        className="chatbot-button"
        style={{
          position: 'fixed',
          bottom: isMobile ? '10px' : '20px',
          right: isMobile ? '10px' : '20px',
          zIndex: 1000,
          backgroundColor: '#4f46e5',
          color: 'white',
          borderRadius: '50%',
          width: isMobile ? '45px' : '60px',
          height: isMobile ? '45px' : '60px',
          border: 'none',
          cursor: 'pointer',
          fontSize: isMobile ? '20px' : '24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 20px rgba(79, 70, 229, 0.4)',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.05)';
          e.currentTarget.style.boxShadow = '0 6px 25px rgba(79, 70, 229, 0.6)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.boxShadow = '0 4px 20px rgba(79, 70, 229, 0.4)';
        }}
      >
        <span style={{ fontSize: isMobile ? '24px' : '28px' }}>🤖</span>
      </button>

      {isOpen && (
        <div
          className="chatbot-container"
          style={{
            position: 'fixed',
            bottom: isMobile ? '70px' : '90px',
            right: isMobile ? '10px' : '20px',
            left: isMobile ? '10px' : 'auto',
            width: isMobile ? 'calc(100% - 20px)' : '400px',
            height: isMobile ? '85vh' : '550px',
            maxHeight: isMobile ? '600px' : '550px',
            backgroundColor: 'white',
            border: '1px solid #e0e0e0',
            borderRadius: isMobile ? '16px' : '12px',
            boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
          }}
        >
          <div
            className="chat-header"
            style={{
              padding: isMobile ? '12px 15px' : '10px',
              backgroundColor: '#007bff',
              color: 'white',
              borderTopLeftRadius: isMobile ? '12px' : '8px',
              borderTopRightRadius: isMobile ? '12px' : '8px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <span className="chat-header-title" style={{ fontWeight: 'bold', fontSize: isMobile ? '16px' : '16px' }}>AI Assistant</span>
            <div style={{ display: 'flex', gap: isMobile ? '8px' : '10px' }}>
              <button
                onClick={startNewChat}
                title="New Chat"
                style={{
                  background: 'none',
                  border: '1px solid rgba(255,255,255,0.3)',
                  color: 'white',
                  borderRadius: '4px',
                  width: isMobile ? '28px' : '30px',
                  height: isMobile ? '28px' : '30px',
                  cursor: 'pointer',
                  fontSize: isMobile ? '14px' : '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                +
              </button>
              <button
                onClick={toggleChat}
                title="Close Chat"
                style={{
                  background: 'none',
                  border: '1px solid rgba(255,255,255,0.3)',
                  color: 'white',
                  borderRadius: '4px',
                  width: isMobile ? '28px' : '30px',
                  height: isMobile ? '28px' : '30px',
                  cursor: 'pointer',
                  fontSize: isMobile ? '14px' : '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                &times;
              </button>
            </div>
          </div>
          <div
            className="chat-messages"
            style={{
              flexGrow: 1,
              padding: isMobile ? '12px' : '15px',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: '#fafafa',
            }}
          >
            {messages.length === 0 && !isLoading && (
              <div className="welcome-container" style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: '#666',
                fontSize: isMobile ? '13px' : '14px',
                textAlign: 'center',
                padding: isMobile ? '15px' : '20px'
              }}>
                <div style={{ fontSize: isMobile ? '40px' : '48px', marginBottom: isMobile ? '12px' : '15px' }}>🤖</div>
                <div className="welcome-title" style={{ fontWeight: 'bold', marginBottom: isMobile ? '6px' : '8px', fontSize: isMobile ? '15px' : '16px' }}>Welcome to AI Assistant!</div>
                <div className="welcome-text" style={{ color: '#888', fontSize: isMobile ? '13px' : '14px', lineHeight: '1.5' }}>
                  I can help you find information in the documentation.<br />
                  Ask me a question to get started!
                </div>
              </div>
            )}
            {messages.map((msg, index) => (
              <div
                key={index}
                className="message-bubble"
                style={{
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  backgroundColor: msg.role === 'user' ? '#dcf8c6' : '#ffffff',
                  borderRadius: '12px',
                  padding: isMobile ? '10px 14px' : '12px 16px',
                  margin: '8px 0',
                  maxWidth: isMobile ? '90%' : '85%',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  border: '1px solid #eee',
                  fontSize: isMobile ? '14px' : 'auto',
                }}
              >
                <div className="message-role" style={{
                  fontWeight: 'bold',
                  fontSize: isMobile ? '11px' : '12px',
                  color: msg.role === 'user' ? '#2ecc71' : '#3498db',
                  marginBottom: '4px'
                }}>
                  {msg.role === 'user' ? 'You' : 'AI Assistant'}
                </div>
                <div style={{ lineHeight: '1.5' }}>
                  {msg.content}
                </div>
                {msg.citations && msg.citations.length > 0 && (
                  <div style={{
                    fontSize: '0.85em',
                    color: '#666',
                    marginTop: '8px',
                    paddingTop: '8px',
                    borderTop: '1px solid #eee'
                  }}>
                    <strong style={{ color: '#555', fontSize: '0.9em' }}>Sources:</strong>
                    <ul style={{ margin: '5px 0 0 0', padding: '0 0 0 15px' }}>
                      {msg.citations.map((cite, idx) => (
                        <li key={idx} style={{ marginBottom: '3px' }}>
                          <a
                            href={`/${cite.source}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              color: '#3498db',
                              textDecoration: 'none',
                              fontSize: '0.9em'
                            }}
                          >
                            {cite.heading ? cite.heading : cite.source}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="message-bubble" style={{
                alignSelf: 'flex-start',
                backgroundColor: '#ffffff',
                borderRadius: '12px',
                padding: isMobile ? '10px 14px' : '12px 16px',
                margin: '8px 0',
                maxWidth: isMobile ? '90%' : '85%',
                boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                border: '1px solid #eee'
              }}>
                <div className="message-role" style={{ fontWeight: 'bold', fontSize: isMobile ? '11px' : '12px', color: '#3498db', marginBottom: '4px' }}>
                  AI Assistant
                </div>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <span>🤔 Thinking</span>
                  <span style={{ marginLeft: '5px' }}><span className="typing-indicator"></span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="chat-input-area" style={{ padding: isMobile ? '12px' : '15px', borderTop: '1px solid #eee', backgroundColor: '#ffffff' }}>
            <div style={{ display: 'flex', gap: isMobile ? '6px' : '8px' }}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                placeholder="Ask a question about the documentation..."
                className="chat-input"
                style={{
                  flexGrow: 1,
                  padding: isMobile ? '10px 12px' : '12px 15px',
                  border: '1px solid #ddd',
                  borderRadius: '20px',
                  fontSize: isMobile ? '14px' : '14px',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#007bff'}
                onBlur={(e) => e.target.style.borderColor = '#ddd'}
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || input.trim() === ''}
                className="send-button"
                style={{
                  backgroundColor: input.trim() === '' || isLoading ? '#cccccc' : '#007bff',
                  color: 'white',
                  border: 'none',
                  borderRadius: '20px',
                  padding: isMobile ? '10px 16px' : '12px 20px',
                  cursor: input.trim() === '' || isLoading ? 'not-allowed' : 'pointer',
                  fontSize: isMobile ? '13px' : '14px',
                  fontWeight: 'bold',
                  minWidth: isMobile ? '50px' : '60px',
                  transition: 'background-color 0.2s',
                }}
              >
                {isLoading ? '...' : 'Send'}
              </button>
            </div>
            <div style={{ fontSize: isMobile ? '10px' : '11px', color: '#999', textAlign: 'center', marginTop: isMobile ? '6px' : '8px' }}>
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
