import Link from "next/link";
import NavLinks from "@/app/ui/common/nav-links";
export default function SideNav() {
  return (
    <>
      <div className="px-6">
        <Link
          className="flex-none text-xl font-semibold text-white focus:outline-none focus:ring-1 focus:ring-gray-600"
          href="/"
          aria-label="Brand"
        >
          KnowledgeNest
        </Link>
      </div>
      <NavLinks />
    </>
  );
}
