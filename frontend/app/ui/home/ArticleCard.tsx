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
    <Card>
      <CardContent className="flex justify-center p-4 pt-0">
        <Image
          src={article.imageUrl}
          alt={article.description}
          width={320}
          height={240}
        />
      </CardContent>
      <h4 className="scroll-m-20 text-sm font-semibold tracking-tight text-center">
        {article.title}
      </h4>
      <CardFooter className="flex justify-between py-5 w-full">
        <Button className="w-24">
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
