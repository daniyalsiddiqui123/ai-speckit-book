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
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (initialSelectedText) {
      setIsOpen(true);
      // Optionally pre-fill input or ask user to confirm question about selected text
    }
  }, [initialSelectedText]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const token = localStorage.getItem('access_token'); // Assuming JWT is stored here
      if (!token) {
        alert('Please log in to use the chatbot.');
        setIsLoading(false);
        return;
      }

      const response = await fetch('http://localhost:8000/api/chat', { // Replace with your backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          question: input,
          conversation_id: conversationId,
          selected_text: initialSelectedText, // Send selected text if available
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');
      let assistantMessageContent = '';
      let assistantCitations: Array<{ source: string; heading?: string }> = [];

      setMessages((prev) => [...prev, { role: 'assistant', content: '', citations: [] }]);

      while (true) {
        const { value, done } = await reader?.read()!;
        if (done) break;

        const chunk = decoder.decode(value);
        // Assuming server sends newline-delimited JSON events
        chunk.split('\n').forEach((jsonString) => {
          if (jsonString.trim()) {
            try {
              const event = JSON.parse(jsonString);
              if (event.type === 'start' && event.conversation_id) {
                setConversationId(event.conversation_id);
              } else if (event.type === 'chunk') {
                assistantMessageContent += event.content;
                setMessages((prev) => {
                  const lastMessage = { ...prev[prev.length - 1] };
                  lastMessage.content = assistantMessageContent;
                  return [...prev.slice(0, prev.length - 1), lastMessage];
                });
              } else if (event.type === 'citation' && event.sources) {
                assistantCitations = event.sources;
                setMessages((prev) => {
                  const lastMessage = { ...prev[prev.length - 1] };
                  lastMessage.citations = assistantCitations;
                  return [...prev.slice(0, prev.length - 1), lastMessage];
                });
              }
            } catch (error) {
              console.error('Failed to parse JSON:', error, jsonString);
            }
          }
        });
      }
    } catch (error) {
      console.error('Chatbot API error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I am having trouble connecting right now.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={toggleChat}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1000,
          backgroundColor: '#007bff',
          color: 'white',
          borderRadius: '50%',
          width: '50px',
          height: '50px',
          border: 'none',
          cursor: 'pointer',
          fontSize: '24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
        }}
      >
        💬
      </button>

      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '350px',
            height: '500px',
            backgroundColor: 'white',
            border: '1px solid #ccc',
            borderRadius: '8px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <div
            style={{
              padding: '10px',
              backgroundColor: '#007bff',
              color: 'white',
              borderTopLeftRadius: '8px',
              borderTopRightRadius: '8px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <span>Chatbot</span>
            <button onClick={toggleChat} style={{ background: 'none', border: 'none', color: 'white', fontSize: '20px', cursor: 'pointer' }}>
              &times;
            </button>
          </div>
          <div
            style={{
              flexGrow: 1,
              padding: '10px',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  backgroundColor: msg.role === 'user' ? '#e0f7fa' : '#f0f0f0',
                  borderRadius: '8px',
                  padding: '8px 12px',
                  margin: '5px 0',
                  maxWidth: '80%',
                }}
              >
                <strong>{msg.role === 'user' ? 'You' : 'Bot'}:</strong> {msg.content}
                {msg.citations && msg.citations.length > 0 && (
                  <div style={{ fontSize: '0.8em', color: '#555', marginTop: '5px' }}>
                    <strong>Sources:</strong>
                    <ul>
                      {msg.citations.map((cite, idx) => (
                        <li key={idx}>
                          {cite.heading ? `${cite.heading} - ` : ''}
                          <a href={`/${cite.source}`} target="_blank" rel="noopener noreferrer">
                            {cite.source}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div style={{ alignSelf: 'flex-start', backgroundColor: '#f0f0f0', borderRadius: '8px', padding: '8px 12px', margin: '5px 0', maxWidth: '80%' }}>
                <strong>Bot:</strong> Thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div style={{ padding: '10px', borderTop: '1px solid #eee', display: 'flex' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  sendMessage();
                }
              }}
              placeholder="Ask a question..."
              style={{ flexGrow: 1, padding: '8px', border: '1px solid #ccc', borderRadius: '4px', marginRight: '10px' }}
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              style={{
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '8px 15px',
                cursor: 'pointer',
              }}
              disabled={isLoading}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
