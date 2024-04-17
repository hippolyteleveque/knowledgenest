import SideNav from "../ui/common/sidenav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
      <SideNav />
      <div className="w-full pt-10 px-4">{children}</div>
    </div>
  );
}
