import Chat from "@/app/ui/chat/chat";
import { fetchConversation } from "@/app/lib/data";

export default async function Page({ params }: { params: { id: string } }) {
  let messages = await fetchConversation(params.id);
  messages = messages.map((msg) => {
    return {
      type: msg.type,
      message: msg.message,
    };
  });
  const lastMessage = messages[messages.length - 1];
  const requestResponse = lastMessage.type === "human";
  return (
    <Chat
      messages={messages}
      conversationId={params.id}
      requestResponse={requestResponse}
    />
  );
}
