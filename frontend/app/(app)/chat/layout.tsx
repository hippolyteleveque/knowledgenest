import ChatNav from "../../ui/chat/chatnav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-screen w-full md:grid-cols-[120px_1fr] lg:grid-cols-[150px_1fr]">
      <ChatNav />
      <div className="w-full">{children}</div>
    </div>
  );
}
