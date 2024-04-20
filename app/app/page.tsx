import ArticleCards from "../ui/home/ArticleCards";
import AddArticleDialog from "../ui/home/add-article-dialog";

export default async function Page() {
  return (
    <main className="flex flex-1 flex-col pt-5">
      <div className="w-40 justify-end">
        <AddArticleDialog />
      </div>
      <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4 p-4 md:gap-8 md:p-8">
        <ArticleCards />
      </div>
    </main>
  );
}
