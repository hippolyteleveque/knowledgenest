import { fetchArticles } from "@/app/lib/data";
import { ArticleCard } from "./ArticleCard";
import { Article } from "@/app/lib/definitions";

export default async function ArticleCards() {
  const articles = await fetchArticles();
  return (
    <>
      {articles.map((article: Article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </>
  );
}
