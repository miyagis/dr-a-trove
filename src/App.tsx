import { useState } from "react";
import { Box } from "@mui/material";
import QuestionInput from "./QuestionInput";
import ConversationSection from "./ConversationSection";
import "./App.css";
import { ChatItemStatus, ChatItemType, IChatItem } from "./ChatItem";
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState<IChatItem[]>([]);

  async function onQuestion(questionText: string) {
    const questionObj = {
      id: Date.now() + ChatItemType.Question,
      type: ChatItemType.Question,
      timestamp: Date.now(),
      content: questionText,
      status: ChatItemStatus.Ready,
    };

    // Add a temporary "pending" answer
    setMessages(prev => [...prev, questionObj, {
      id: questionObj.id + ChatItemType.Answer,
      type: ChatItemType.Answer,
      timestamp: Date.now(),
      content: "Generating...",
      status: ChatItemStatus.Pending,
    }]);

    try {
      // Send POST request to Flask backend
      const response = await axios.post('/api/answer', { question: questionText });

      // Update state with received answer
      setMessages(prev => prev.map(chatItem => {
        if (chatItem.id === questionObj.id + ChatItemType.Answer) {
          return {
            ...chatItem,
            content: response.data.answer,
            status: ChatItemStatus.Ready,
          };
        }
        return chatItem;
      }));
    } catch (error) {
      console.error('Error fetching answer:', error);
      // Update state with error message (optional)
    }
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
      }}
      justifyContent="center"
    >
      <ConversationSection messages={messages} />
      <QuestionInput onQuestion={onQuestion} />
    </Box>
  );
}

export default App;
