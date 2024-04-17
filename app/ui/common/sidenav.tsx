import Link from "next/link";

import NavLinks from "@/app/ui/common/nav-links";
export default function SideNav() {
  return (
    <div className="border-r bg-muted/40 md:block">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-bold">
            <span className="">KnowledgeNest</span>
          </Link>
        </div>

        <NavLinks />
      </div>
    </div>
  );
}
