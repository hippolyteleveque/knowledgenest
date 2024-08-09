"use client";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { sendChatMessage } from "@/app/lib/actions";

export default function Page() {
  const [currUserMsg, setCurrUserMsg] = useState("");
  const [messages, setMessages] = useState<any>([]);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setMessages((msgs) => [...msgs, { type: "human", content: currUserMsg }]);
    setCurrUserMsg("");
    const msg = await sendChatMessage(currUserMsg);
    setMessages((msgs) => [...msgs, { type: "ai", content: msg }]);
  };

  const formatMessage = (msg: any) => {
    if (msg.type === "human") {
      return (
        <div className="flex flex-row-reverse items-start gap-4">
          <div className="rounded-lg bg-gray-900 p-4 text-sm text-gray-50 dark:bg-gray-50 dark:text-gray-900">
            <p>{msg.content}</p>
          </div>
        </div>
      );
    } else {
      return (
        <div className="flex items-start gap-4">
          <div className="rounded-lg bg-gray-100 p-4 text-sm dark:bg-gray-800">
            <p>{msg.content}</p>
          </div>
        </div>
      );
    }
  };

  const msgs = messages.map((el) => formatMessage(el));

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
              value={currUserMsg}
              onChange={(e) => setCurrUserMsg(e.target?.value)}
            />
            <Button type="submit">Send</Button>
          </form>
        </div>
      </div>
    </main>
  );
}
