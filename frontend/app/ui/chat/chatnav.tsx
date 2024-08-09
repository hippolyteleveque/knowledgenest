import Link from "next/link";

export default function ChatNav() {
  return (
    <>
      <div className="flex-1 overflow-auto">
        <div className="grid gap-1 p-2 text-foreground">
          <div className="px-2 text-xs font-medium text-muted-foreground">
            Today
          </div>
          <Link
            href="#"
            className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
            prefetch={false}
          >
            Airplane Turbulence: Sky&apos;s Rollercoaster
          </Link>
          <Link
            href="#"
            className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
            prefetch={false}
          >
            How to make a chat app with React
          </Link>
          <Link
            href="#"
            className="flex-1 block p-2 overflow-hidden text-sm truncate transition-colors rounded-md whitespace-nowrap hover:bg-muted/50"
            prefetch={false}
          >
            Cooking recipe for disaster
          </Link>
        </div>
      </div>
    </>
  );
}
