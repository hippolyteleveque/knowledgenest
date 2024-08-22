"use client";

import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { usePathname } from "next/navigation";

export default function ContentPagination({
  currentPage,
  numPages,
}: {
  currentPage: number;
  numPages: number;
}) {
  const pathname = usePathname();
  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          {currentPage > 1 && (
            <PaginationPrevious href={`${pathname}?page=${currentPage - 1}`} />
          )}
        </PaginationItem>
        <PaginationItem>
          {currentPage < numPages && (
            <PaginationNext href={`${pathname}?page=${currentPage + 1}`} />
          )}
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
}
