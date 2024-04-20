import ArticleCards from "../ui/home/ArticleCards";

export default async function Page() {
  return (
    <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
      <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
        <ArticleCards />
      </div>
    </main>
  );
}
