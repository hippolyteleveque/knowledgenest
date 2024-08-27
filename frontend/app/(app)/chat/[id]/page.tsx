import Chat from "@/app/ui/chat/chat";
import { fetchConversation, fetchSources } from "@/app/lib/data";
import ChatSources from "@/app/ui/chat/chat-sources";
import ChatManager from "@/app/ui/chat/chat-manager";

export default async function Page({ params }: { params: { id: string } }) {
  let messages = await fetchConversation(params.id);
  const sources = await fetchSources(params.id);
  messages = messages.map((msg) => {
    return {
      type: msg.type,
      message: msg.message,
    };
  });
  const lastMessage = messages[messages.length - 1];
  const requestResponse = lastMessage.type === "human";

  return (
    <ChatManager
      messages={messages}
      conversationId={params.id}
      requestResponse={requestResponse}
      sources={sources}
    />
  );
}
