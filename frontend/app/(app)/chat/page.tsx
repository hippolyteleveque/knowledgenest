"use client";
import { Button } from "@/components/ui/button";
import { FormEvent, useState } from "react";
import { Input } from "@/components/ui/input";
import { startConversation } from "@/app/lib/actions";
import { usePathname, useRouter } from "next/navigation";
import { ChatMessage } from "@/app/lib/definitions";

export default function Page() {
  const [currUserMsg, setCurrUserMsg] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const pathname = usePathname();
  const { replace } = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (currUserMsg) {
      setMessages((msgs) => [...msgs, { type: "human", message: currUserMsg }]);
      setCurrUserMsg(null);
      const { id: conversationId } = await startConversation(currUserMsg);
      replace(`${pathname}/${conversationId}`);
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
        <div className="border-t bg-gray-100 rounded-lg px-4 py-4 my-10 jdark:bg-gray-900 ">
          <form className="flex items-center gap-2" onSubmit={handleSubmit}>
            <Input
              type="text"
              placeholder="Type your message..."
              // className="flex-1"
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
