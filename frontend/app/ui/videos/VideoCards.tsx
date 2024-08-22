import { VideoCard } from "./VideoCard";
import { Video } from "@/app/lib/definitions";

export default async function VideoCards({
  videos,
}: {
  videos: Video[];
}) {
  return (
    <>
      {videos.map((video: Video) => (
        <VideoCard key={video.id} video={video} />
      ))}
    </>
  );
}
