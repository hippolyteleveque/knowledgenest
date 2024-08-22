import ArticleCards from "../../ui/home/ArticleCards";
import AddArticleDialog from "../../ui/home/add-article-dialog";
import ContentPagination from "../../ui/common/pagination";
import { fetchArticles } from "@/app/lib/data";

const ITEMS_PER_PAGE = 8;

export default async function Page({
  searchParams,
}: {
  searchParams?: { page?: number };
}) {
  const currentPage = Number(searchParams?.page) || 1;
  const { articles, numArticles } = await fetchArticles(
    currentPage,
    ITEMS_PER_PAGE,
  );
  const numPages = Math.ceil(numArticles / ITEMS_PER_PAGE);
  return (
    <main className="flex flex-1 flex-col pt-5">
      <div className="w-40 justify-end">
        <AddArticleDialog />
      </div>
      <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4 p-4 md:gap-8 md:p-8">
        <ArticleCards articles={articles} />
      </div>
      <div className="pt-5">
        <ContentPagination currentPage={currentPage} numPages={numPages} />
      </div>
    </main>
  );
}
