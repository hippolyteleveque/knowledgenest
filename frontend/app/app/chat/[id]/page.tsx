import { useRouter } from "next/navigation";
import Chat from "@/app/ui/chat/chat";
import { fetchConversation } from "@/app/lib/data";

export default async function Page({ params }: { params: { id: string } }) {
  let messages = await fetchConversation(params.id);
  messages = messages.map((msg) => {
    return {
      type: msg.type,
      content: msg.message,
    };
  });
  return <Chat messages={messages} conversationId={params.id}/>;
}
