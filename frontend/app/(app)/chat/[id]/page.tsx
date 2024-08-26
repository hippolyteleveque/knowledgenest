import Chat from "@/app/ui/chat/chat";
import { fetchConversation } from "@/app/lib/data";
import ChatSources from "@/app/ui/chat/chat-sources";

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
    <div className="grid min-h-screen w-full md:grid-cols-[1fr_175px] lg:grid-cols-[1fr_250px]">
      <Chat
        messages={messages}
        conversationId={params.id}
        requestResponse={requestResponse}
      />
      <ChatSources conversationId={params.id} />
    </div>
  );
}
