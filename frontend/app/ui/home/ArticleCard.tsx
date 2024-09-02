"use client";

import * as React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import Image from "next/image";
import { Article } from "@/app/lib/definitions";
import { deleteArticle } from "@/app/lib/actions";

export function ArticleCard({ article }: { article: Article }) {
  const deleteArticleWithId = deleteArticle.bind(null, article.id);
  const handleArticleDeletion = async () => await deleteArticleWithId();
  return (
    <Card className="max-w-[280px] flex flex-col">
      <CardContent className="p-4 pt-0 flex-grow">
        <div className="relative w-full h-48 mb-2">
          <Image
            src={article.imageUrl}
            alt={article.description}
            fill
            objectFit="cover"
            className="rounded-md"
          />
        </div>
        <h4 className="scroll-m-20 text-sm font-semibold tracking-tight text-center line-clamp-2">
          {article.title}
        </h4>
      </CardContent>
      <CardFooter className="flex justify-between py-3 w-full">
        <Button className="w-24" asChild>
          <a href={article.url}>View</a>
        </Button>
        <Button
          variant="outline"
          onClick={handleArticleDeletion}
          className="w-24"
        >
          Delete
        </Button>
      </CardFooter>
    </Card>
  );
}
