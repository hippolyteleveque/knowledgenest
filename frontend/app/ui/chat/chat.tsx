"use client";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { ChatMessage } from "@/app/lib/definitions";
import Cookies from "js-cookie";

type ChatProps = {
  messages: ChatMessage[];
  conversationId: string;
};

export default function Chat(props: ChatProps) {
  const [currUserMsg, setCurrUserMsg] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>(props.messages);
  const [socket, setSocket] = useState<any>(null);

  useEffect(() => {
    const token = Cookies.get("jwtToken");
    console.log(token);
    const ws = new WebSocket(
      `ws://localhost:8000/api/v1/chat/${props.conversationId}/ws?token=${token}`
    );
    setSocket(ws);

    ws.onopen = () => {};

    ws.onmessage = (event) => {
      if (event.data === "<START>") {
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: "ai", message: "" },
        ]);
      } else {
        setMessages((prevMessages) => {
          const lastAiMessage = prevMessages[prevMessages.length - 1];
          const newAiMessage = {
            ...lastAiMessage,
            message: lastAiMessage.message + event.data,
          };
          const previousMessages = prevMessages.slice(0, -1);
          return [...previousMessages, newAiMessage];
        });
      }
    };

    ws.onclose = () => {};

    return () => {
      ws.close();
    };
  }, []);

  // const handleSubmit = async (e: any) => {
  //   e.preventDefault();
  //   if (currUserMsg) {
  //     setMessages((msgs) => [...msgs, { type: "human", message: currUserMsg }]);
  //     setCurrUserMsg("");
  //     const msg = await sendChatMessage(currUserMsg, props.conversationId);
  //     setMessages((msgs) => [...msgs, { type: "ai", message: msg }]);
  //   }
  // };
  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (currUserMsg) {
      socket.send(currUserMsg);
      setMessages((msgs) => [...msgs, { type: "human", message: currUserMsg }]);
      setCurrUserMsg("");
    }
  };

  const formatMessage = (msg: ChatMessage, i: number) => {
    if (msg.type === "human") {
      return (
        <div className="flex flex-row-reverse items-start gap-4" key={i}>
          <div className="rounded-lg bg-gray-900 p-4 text-sm text-gray-50 dark:bg-gray-50 dark:text-gray-900">
            <p>{msg.message}</p>
          </div>
        </div>
      );
    } else {
      return (
        <div className="flex items-start gap-4" key={i}>
          <div className="rounded-lg bg-gray-100 p-4 text-sm dark:bg-gray-800">
            <p>{msg.message}</p>
          </div>
        </div>
      );
    }
  };

  const msgs = messages.map((el, i) => formatMessage(el, i));

  return (
    <main>
      <div className="flex h-screen flex-col flex-1 pt-5">
        <main className="flex-1 overflow-auto">
          <div className="mx-auto max-w-3xl space-y-4 p-4">{msgs}</div>
        </main>
        <div className="border-t bg-gray-100 rounded-lg px-4 py-4 my-10 jdark:bg-gray-900">
          <form className="flex items-center gap-2" onSubmit={handleSubmit}>
            <Input
              type="text"
              placeholder="Type your message..."
              className="flex-1"
              id="message"
              name="message"
              value={currUserMsg ? currUserMsg : ""}
              onChange={(e) => setCurrUserMsg(e.target?.value)}
            />
            <Button type="submit">Send</Button>
          </form>
        </div>
      </div>
    </main>
  );
}
