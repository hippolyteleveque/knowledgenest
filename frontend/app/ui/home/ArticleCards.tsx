import { ArticleCard } from "./ArticleCard";
import { Article } from "@/app/lib/definitions";

export default async function ArticleCards({
  articles,
}: {
  articles: Article[];
}) {
  return (
    <>
      {articles.map((article: Article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </>
  );
}
