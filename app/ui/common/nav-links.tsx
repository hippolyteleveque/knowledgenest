"use client";

import Link from "next/link";
import clsx from "clsx";
import {
  HomeIcon,
  CpuChipIcon,
  Cog8ToothIcon,
} from "@heroicons/react/24/outline";
import { usePathname } from "next/navigation";

const links = [
  { name: "Home", href: "/app", icon: HomeIcon },
  {
    name: "Chat",
    href: "/app/chat",
    icon: CpuChipIcon,
  },
  {
    name: "Settings",
    href: "/app/settings",
    icon: Cog8ToothIcon,
  },
];

export default function NavLinks() {
  const pathname = usePathname();
  return (
    <nav
      className="hs-accordion-group p-6 w-full flex flex-col flex-wrap"
      data-hs-accordion-always-open
    >
      <ul className="space-y-4">
        {links.map((link) => {
          const LinkIcon = link.icon;
          return (
            <li key={link.name}>
              <Link
                href={link.href}
                className={clsx(
                  "flex items-center gap-x-3 py-2 px-2.5 text-sm text-gray-400 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-600",
                  {
                    "text-white bg-gray-700": pathname == link.href,
                  },
                )}
              >
                <LinkIcon className="flex-shrink-0 size-5" />
                <p> {link.name}</p>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
