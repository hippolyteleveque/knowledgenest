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
      <CardContent>
        <Image
          src={article.imageUrl}
          alt={article.description}
          width={200}
          height={200}
        />
      </CardContent>
      <h4 className="scroll-m-20 text-sm font-semibold tracking-tight text-center">
        {article.title}
      </h4>
      <CardFooter className="flex justify-center py-5 w-50">
        <Button variant="outline">
          <a href={article.url}>View</a>
        </Button>
        <Button onClick={handleArticleDeletion}>Delete</Button>
      </CardFooter>
    </Card>
  );
}
