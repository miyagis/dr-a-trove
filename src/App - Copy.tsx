import { useState } from "react";
import { Box } from "@mui/material";
import QuestionInput from "./QuestionInput";
import ConversationSection from "./ConversationSection";
import "./App.css";
import { ChatItemStatus, ChatItemType, IChatItem } from "./ChatItem";

// const seed = [
// 	{ id: Date.now() + ChatItemType.Question, type: ChatItemType.Question, timestamp: Date.now(), content: "Hi there", status: ChatItemStatus.Ready },
// 	{ id: Date.now() + ChatItemType.Answer, type: ChatItemType.Answer, timestamp: Date.now()+1, content: "Hi", status: ChatItemStatus.Ready },
// ];

function App() {
	const [messages, setMessages] = useState<IChatItem[]>([]);

	const onQuestion = (questionText: string) => {

        // TODO: create a function to create ChatItem objects
        // TODO: generate unique ID, should come from backend
        const questionObj = {
            id: Date.now() + ChatItemType.Question,
            type: ChatItemType.Question,
            timestamp: Date.now(),
            content: questionText,
            status: ChatItemStatus.Ready
        }

        const answerObj = {
            id: Date.now() + ChatItemType.Answer,
            type: ChatItemType.Answer,
            timestamp: Date.now(),
            content: "Generating",
            status: ChatItemStatus.Pending
        }

        setMessages(prev => [...prev, questionObj, answerObj])

        // TODO: in current form will be more effective to just use general "loading" state
        setTimeout(() => setMessages(prev => prev.map( chatItem => {
            if(chatItem.id !== answerObj.id)
                return chatItem;

            return {...answerObj, status: ChatItemStatus.Ready, content: "This is the answer"}
        })), 2000 )
    };
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
			<QuestionInput onQuestion={onQuestion}/>
		</Box>
	);
}

export default App;
