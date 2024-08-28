import { useState } from "react";
import styles from "./QuestionInput.module.css";
import { IconButton, TextField } from "@mui/material";
import { Send } from "@mui/icons-material";

function QuestionInput(props: { onQuestion: (questionText: string) => void }) {
	const [question, setQuestion] = useState("");

	const _onQuestion = (questionText: string) => {
		props.onQuestion(questionText);
		setQuestion("");
	};

	const onKeyPress = (key: string) => {
		if (key === "Enter") {
			_onQuestion(question);
            setQuestion("");
		}
	};

	return (
		<div className={styles.QuestionInput}>
			<TextField
				className={styles.textField}
				id="question-input"
				placeholder="Ask question"
				value={question}
				size="small"
				onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={(event) => onKeyPress(event.key)}
			/>
			<IconButton
				className={styles.sendIconButton}
				color="primary"
				aria-label="send message"
				size="small"
				onClick={() => _onQuestion(question)}
			>
				<Send />
			</IconButton>
		</div>
	);
}

export default QuestionInput;
