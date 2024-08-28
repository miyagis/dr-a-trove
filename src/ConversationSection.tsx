import { styled } from '@mui/material/styles';
import { Paper } from '@mui/material'
import ChatItem, { ChatItemType, IChatItem } from './ChatItem';

const MessagesContainer = styled(Paper)(({ theme }) => ({
	backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
	...theme.typography.body2,
	padding: theme.spacing(1),
	color: theme.palette.text.secondary,
	flex: 1
}));

function ConversationSection({messages}: {messages: IChatItem[]}) {

	return (
		<MessagesContainer sx={{
			display: 'flex',
			flexDirection: "column",
            paddingTop: '1rem'
		}} elevation={0}>
            {messages.map(message => (
                <ChatItem key={message.id} {...message}/>
            ))}
		</MessagesContainer>
	)
}

export default ConversationSection
