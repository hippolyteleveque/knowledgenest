"use client";
import { fetchSources } from "@/app/lib/client";
import { ChatMessage } from "@/app/lib/definitions";
import Chat from "@/app/ui/chat/chat";
import ChatSources from "@/app/ui/chat/chat-sources";
import { useCallback, useState } from "react";
import Cookies from "js-cookie"

type ChatManagerProps = {
  conversationId: string;
  messages: ChatMessage[];
  requestResponse: boolean;
  sources: any[];
};

export default function ChatManager(props: ChatManagerProps) {
  const [sources, setSources] = useState<any[]>(props.sources);

  const chatCallback = useCallback(async () => {
    const token = Cookies.get("jwtToken"); 
    const refreshedSources = await fetchSources(props.conversationId, token!);
    setSources(refreshedSources);
  }, [props.conversationId]);

  return (
    <div className="grid min-h-screen w-full md:grid-cols-[1fr_175px] lg:grid-cols-[1fr_250px]">
      <Chat
        messages={props.messages}
        conversationId={props.conversationId}
        requestResponse={props.requestResponse}
        chatCallback={chatCallback}
      />
      <ChatSources rawSources={sources} />
    </div>
  );
}
