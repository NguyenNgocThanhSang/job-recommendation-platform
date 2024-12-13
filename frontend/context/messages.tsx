import React, { createContext, useContext, useState, ReactNode } from 'react';

// Define the shape of your message data
interface Message {
  id: number;
  text: string;
  sender: string;
  timestamp: Date;
}

// Define the context type
interface MessagesContextType {
  messages: Message[];
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  removeMessage: (id: number) => void;
  // Add more functions as needed
}

// Create the context with a default value
const MessagesContext = createContext<MessagesContextType | undefined>(undefined);

// Provider component
interface MessagesProviderProps {
  children: ReactNode;
}

export const MessagesProvider: React.FC<MessagesProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);

  // Function to add a new message
  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      id: messages.length + 1, // Simple ID generation; consider using UUIDs for production
      text: message.text,
      sender: message.sender,
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  // Function to remove a message by ID
  const removeMessage = (id: number) => {
    setMessages((prevMessages) => prevMessages.filter((msg) => msg.id !== id));
  };

  // You can add more functions to handle message updates, etc.

  return (
    <MessagesContext.Provider value={{ messages, addMessage, removeMessage }}>
      {children}
    </MessagesContext.Provider>
  );
};

// Custom hook for consuming the MessagesContext
export const useMessages = (): MessagesContextType => {
  const context = useContext(MessagesContext);
  if (!context) {
    throw new Error('useMessages must be used within a MessagesProvider');
  }
  return context;
};
