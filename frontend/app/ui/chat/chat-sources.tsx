"use client";
import { Card, CardContent } from "@/components/ui/card";
import Image from "next/image";
import { fetchSources } from "@/app/lib/data";

type ChatSourcesProps = {
  rawSources: any;
};

type Source = {
  id: string;
  url: string;
  imageUrl: string;
  description: string;
  title: string;
  score: number;
};

export default function ChatSources(props: ChatSourcesProps) {
  // const rawSources = await fetchSources(props.conversationId);
  const rawSources = props.rawSources;
  const allSources = [...rawSources.videos, ...rawSources.articles];
  const sources: Source[] = allSources.reduce(
    (uniqueSources: Source[], newSource: Source) => {
      // ensure there is no duplicate, keep the highest score, can be removed
      const idx = uniqueSources.findIndex((el) => el.id === newSource.id);
      if (idx === -1) {
        uniqueSources.push(newSource);
      } else {
        uniqueSources[idx].score = Math.max(
          uniqueSources[idx].score,
          newSource.score
        );
      }
      return uniqueSources;
    },
    []
  );
  // sort the sources by score
  sources.sort((sourceA, sourceB) => sourceB.score - sourceA.score);

  return (
    <div className="border-l md:block">
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6 items-center font-bold">
        <span>Sources</span>
      </div>
      <div className="flex max-h-[calc(100vh-100px)] flex-col px-4 overflow-auto">
        {sources.map((source) => (
          <a href={source.url} className="py-5" key={source.id}>
            <Card>
              <CardContent className="flex justify-center">
                <Image
                  src={source.imageUrl}
                  alt={source.description}
                  width={200}
                  height={150}
                />
              </CardContent>
              <h4 className="scroll-m-20 text-sm font-semibold tracking-tight text-center">
                {source.title.slice(0, 30)}
              </h4>
            </Card>
          </a>
        ))}
      </div>
    </div>
  );
}
