import styles from "./ChatItem.module.css";
import { Box, CircularProgress } from "@mui/material";
import { Send } from "@mui/icons-material";
import cx from "classnames";

export enum ChatItemStatus {
    Ready = "ready",
    Pending = "pending"
}

export enum ChatItemType {
	Answer = "answer",
	Question = "question",
}

export interface IChatItem {
    id: string,
	type: ChatItemType;
    timestamp: number;
    content: string;
    status: ChatItemStatus;
}

function ChatItem(props: IChatItem) {
	const className = cx(styles.ChatItem, styles[props.type]);

	return (
        <Box className={className}>
            {props.status === ChatItemStatus.Pending && <CircularProgress sx={{marginRight: '10px'}} size={15}/>}
            {props.content}
        </Box>
    );
}

export default ChatItem;
