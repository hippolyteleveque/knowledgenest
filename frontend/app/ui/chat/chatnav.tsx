import Link from "next/link";
import { fetchConversations } from "@/app/lib/data";
import { CirclePlus } from "lucide-react";
import { ChatConversation } from "@/app/lib/definitions";

function isSameDay(date1: Date, date2: Date) {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
}

export default async function ChatNav() {
  // TODO handle pagination
  const conversations = await fetchConversations();

  function categorizeData(data: ChatConversation[]): {
    today: ChatConversation[];
    yesterday: ChatConversation[];
    lastWeek: ChatConversation[];
    before: ChatConversation[];
  } {
    const today = new Date();
    const yesterday = new Date();
    yesterday.setDate(today.getDate() - 1);
    const lastWeek = new Date();
    lastWeek.setDate(today.getDate() - 7);

    const result: {
      today: ChatConversation[];
      yesterday: ChatConversation[];
      lastWeek: ChatConversation[];
      before: ChatConversation[];
    } = {
      today: [],
      yesterday: [],
      lastWeek: [],
      before: [],
    };

    data.forEach((item) => {
      const createdAt = new Date(item.created_at);
      if (isSameDay(createdAt, today)) {
        result.today.push(item);
      } else if (isSameDay(createdAt, yesterday)) {
        result.yesterday.push(item);
      } else if (createdAt >= lastWeek && createdAt < yesterday) {
        result.lastWeek.push(item);
      } else {
        result.before.push(item);
      }
    });

    return result;
  }

  const sortedData = categorizeData(conversations);

  return (
    <>
      <div className="flex-1 overflow-auto mt-3">
        <div className="grid gap-1 p-2 text-foreground">
          <div className="flex justify-center">
            <Link href="/chat">
              <CirclePlus className="h-6 w-6 text-primary" />
            </Link>
          </div>
          <div className="overflow-y-auto max-h-[calc(100vh-100px)]">
            {sortedData.today.length > 0 && (
              <>
                <div className="px-2 text-xs font-medium text-muted-foreground">
                  Today
                </div>
                {sortedData.today.map((conv) => {
                  return (
                    <Link
                      href={`/chat/${conv.id}`}
                      className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
                      key={conv.id}
                    >
                      {conv.name}
                    </Link>
                  );
                })}
              </>
            )}
            {sortedData.yesterday.length > 0 && (
              <>
                <div className="px-2 text-xs font-medium text-muted-foreground">
                  Yesterday
                </div>
                {sortedData.yesterday.map((conv) => {
                  return (
                    <Link
                      href={`/chat/${conv.id}`}
                      className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
                      key={conv.id}
                    >
                      {conv.name}
                    </Link>
                  );
                })}
              </>
            )}
            {sortedData.lastWeek.length > 0 && (
              <>
                <div className="px-2 text-xs font-medium text-muted-foreground">
                  Last Week
                </div>
                {sortedData.lastWeek.map((conv) => {
                  return (
                    <Link
                      href={`/chat/${conv.id}`}
                      className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
                      key={conv.id}
                    >
                      {conv.name}
                    </Link>
                  );
                })}
              </>
            )}
            {sortedData.before.length > 0 && (
              <>
                <div className="px-2 text-xs font-medium text-muted-foreground">
                  Older
                </div>
                {sortedData.before.map((conv) => {
                  return (
                    <Link
                      href={`/chat/${conv.id}`}
                      className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
                      key={conv.id}
                    >
                      {conv.name}
                    </Link>
                  );
                })}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
