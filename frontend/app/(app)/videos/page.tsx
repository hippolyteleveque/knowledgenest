import ContentPagination from "@/app/ui/common/pagination";
import { fetchVideos } from "@/app/lib/data";
import AddVideoDialog from "@/app/ui/videos/add-video-dialog";
import VideoCards from "@/app/ui/videos/VideoCards";

const ITEMS_PER_PAGE = 8;

export default async function Page({
  searchParams,
}: {
  searchParams?: { page?: number };
}) {
  const currentPage = Number(searchParams?.page) || 1;
  const { videos, numVideos } = await fetchVideos(
    currentPage,
    ITEMS_PER_PAGE,
  );
  const numPages = Math.ceil(numVideos / ITEMS_PER_PAGE);
  return (
    <main className="flex flex-1 flex-col pt-5 px-4">
      <div className="w-40 justify-end">
        <AddVideoDialog />
      </div>
      <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4 p-4 md:gap-8 md:p-8">
        <VideoCards videos={videos} />
      </div>
      <div className="pt-5">
        <ContentPagination currentPage={currentPage} numPages={numPages} />
      </div>
    </main>
  );
}
