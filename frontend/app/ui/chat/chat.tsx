"use client";
import { Button } from "@/components/ui/button";
import { useState, useEffect, useRef } from "react";
import { Input } from "@/components/ui/input";
import { ChatMessage } from "@/app/lib/definitions";
import Cookies from "js-cookie";
import { marked } from "marked";

type ChatProps = {
  messages: ChatMessage[];
  conversationId: string;
  requestResponse: boolean;
  chatCallback: () => void;
};

export default function Chat(props: ChatProps) {
  const [currUserMsg, setCurrUserMsg] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>(props.messages);
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isWaitingMessage, setIsWaitingMessage] = useState<boolean>(
    props.requestResponse
  );
  const chatRef = useRef<any>(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
    const token = Cookies.get("jwtToken");
    const ws = new WebSocket(
      `${process.env.NEXT_PUBLIC_WEBSOCKET_HOST}/api/v1/chat/${props.conversationId}/ws?token=${token}`
    );
    setSocket(ws);

    ws.onopen = () => {
      if (props.requestResponse) {
        ws.send("<START>"); // TODO make that better
      }
    };

    ws.onmessage = (event) => {
      if (event.data === "<START>") {
        // We call the callback
        props.chatCallback();
        // we initiate the message
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: "ai", message: "" },
        ]);
        // No more waiting
        setIsWaitingMessage((prevState) => false);
      } else {
        const data = JSON.parse(event.data);
        if ("output" in data) {
          setMessages((prevMessages) => {
            const lastAiMessage = prevMessages[prevMessages.length - 1];
            const newAiMessage = {
              ...lastAiMessage,
              message: lastAiMessage.message + data.output,
            };
            const previousMessages = prevMessages.slice(0, -1);
            return [...previousMessages, newAiMessage];
          });
        }
      }
      if (chatRef.current) {
        chatRef.current.scrollTop = chatRef.current.scrollHeight;
      }
    };

    ws.onclose = () => {};

    return () => {
      ws.close();
    };
  }, [props.conversationId, props.requestResponse, props.chatCallback]);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (currUserMsg && socket) {
      socket.send(currUserMsg);
      setMessages((msgs) => [...msgs, { type: "human", message: currUserMsg }]);
      setCurrUserMsg(null);
      // We are now waiting for AI message
      setIsWaitingMessage(true);
    }
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  };

  const formatMessage = (msg: ChatMessage, i: number) => {
    if (msg.type === "human") {
      return (
        <div className="flex flex-row-reverse items-start gap-4" key={i}>
          <div className="rounded-lg bg-gray-900 p-4 text-sm text-gray-50 bg-primary">
            <p>{msg.message}</p>
          </div>
        </div>
      );
    } else {
      return (
        <div className="flex items-start gap-4" key={i}>
          <div className="rounded-lg bg-gray-100 pt-4 pr-4 pl-4 text-sm dark:bg-gray-800 w-full">
            {/* Remove the pre tag and use a div with whitespace-pre-wrap */}
            <div
              className="whitespace-pre-wrap font-sans"
              dangerouslySetInnerHTML={{
                __html: marked.parse(msg.message, { breaks: true }),
              }}
            />
          </div>
        </div>
      );
    }
  };

  const msgs = messages.map((el, i) => formatMessage(el, i));

  return (
    <main>
      <div className="flex h-screen flex-col flex-1 pt-5">
        <main className="flex-1 overflow-auto" ref={chatRef}>
          <div className="mx-auto max-w-3xl space-y-4 p-4">
            {msgs}
            {isWaitingMessage ? (
              <div className="flex items-start gap-4">
                <div className="flex gap-2 rounded-lg bg-gray-100 p-4 dark:bg-gray-800">
                  <div className="h-2 w-2 bg-black rounded-full animate-bounce [animation-delay:-1s]"></div>
                  <div className="h-2 w-2 bg-black rounded-full animate-bounce [animation-delay:-0.035s]"></div>
                  <div className="h-2 w-2 bg-black rounded-full animate-bounce"></div>
                </div>
              </div>
            ) : null}
          </div>
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
