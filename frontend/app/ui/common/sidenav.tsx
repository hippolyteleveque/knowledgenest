import Link from "next/link";

import NavLinks from "@/app/ui/common/nav-links";
import { Button } from "@/components/ui/button";
import { logout } from "@/app/lib/actions";

export default async function SideNav() {
  return (
    <div className="border-r bg-muted/40 md:block">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-bold">
            <span> KnowledgeNest</span>
          </Link>
        </div>
        <NavLinks />
        <form className="justify-center mb-5 flex" action={logout}>
          <Button className="w-40" type="submit">
            Logout
          </Button>
        </form>
      </div>
    </div>
  );
}
