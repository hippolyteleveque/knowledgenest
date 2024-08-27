"use client";

import * as React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import Image from "next/image";
import { Video } from "@/app/lib/definitions";
import { deleteVideo } from "@/app/lib/actions";

export function VideoCard({ video }: { video: Video }) {
  const deleteVideoWithId = deleteVideo.bind(null, video.id);
  const handleVideoDeletion = async () => await deleteVideoWithId();
  return (
    <Card>
      <CardContent className="flex justify-center p-4 pt-0">
        <Image
          src={video.imageUrl}
          alt={video.description}
          width={320}
          height={240}
        />
      </CardContent>
      <h4 className="scroll-m-20 text-sm font-semibold tracking-tight text-center">
        {video.title}
      </h4>
      <CardFooter className="flex justify-between py-5 w-full">
        <Button className="w-24">
          <a href={video.url}>View</a>
        </Button>
        <Button
          variant="outline"
          onClick={handleVideoDeletion}
          className="w-24"
        >
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
}
