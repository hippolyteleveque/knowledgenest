import * as React from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import Image from "next/image";
import { Article } from "@/app/lib/definitions";

export function ArticleCard({ article }: { article: Article }) {
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
      </CardFooter>
    </Card>
  );
}
