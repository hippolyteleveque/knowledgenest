import Link from "next/link";
import { fetchConversations } from "@/app/lib/data";
import { CirclePlus } from "lucide-react";

export default async function ChatNav() {
  const conversations = await fetchConversations();
  return (
    <>
      <div className="flex-1 overflow-auto mt-3">
        <div className="grid gap-1 p-2 text-foreground">
          <div className="flex justify-center">
            <Link href="/app/chat">
              <CirclePlus className="h-6 w-6" />
            </Link>
          </div>
          <div className="px-2 text-xs font-medium text-muted-foreground">
            Today
          </div>
          {conversations.map((conv) => {
            return (
              <Link
                href={`/app/chat/${conv.id}`}
                className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
                key={conv.id}
              >
                {conv.name}
              </Link>
            );
          })}
        </div>
      </div>
    </>
  );
}
