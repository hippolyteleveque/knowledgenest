"use client";

import Link from "next/link";
import clsx from "clsx";
import { Newspaper, Settings, Cpu, Youtube } from "lucide-react";

import { usePathname } from "next/navigation";

const links = [
  { name: "Articles", href: "/articles", icon: Newspaper },
  { name: "Youtube", href: "/videos", icon: Youtube },
  {
    name: "Chat",
    href: "/chat",
    icon: Cpu,
  },
  {
    name: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function NavLinks() {
  const pathname = usePathname();
  return (
    <div className="flex-1">
      <nav
        className="grid items-start px-2 text-sm font-medium lg:px-4"
        data-hs-accordion-always-open
      >
        {links.map((link) => {
          const LinkIcon = link.icon;
          return (
            <Link
              key={link.name}
              href={link.href}
              className={clsx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary",
                {
                  "text-primary bg-muted font-semibold": pathname == link.href,
                }
              )}
            >
              <LinkIcon className="h-4 w-4" />
              <p> {link.name}</p>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
