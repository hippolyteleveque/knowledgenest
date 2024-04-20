import { fetchArticles } from "@/app/lib/data";
import { ArticleCard } from "./ArticleCard";

export default async function ArticleCards() {
  const articles = await fetchArticles();
  return (
    <>
      {articles.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </>
  );
}
