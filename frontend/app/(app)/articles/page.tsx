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
    <main className="flex flex-1 flex-col pt-5 px-4">
      <div className="w-40 justify-end">
        <AddArticleDialog />
      </div>
      <div className="grid gap-2 md:grid-cols-2 md:gap-4 lg:grid-cols-4 p-2 md:gap-4 md:p-4">
        <ArticleCards articles={articles} />
      </div>
      <div className="pt-5">
        <ContentPagination currentPage={currentPage} numPages={numPages} />
      </div>
    </main>
  );
}
