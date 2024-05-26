import { cookies } from "next/headers";

export async function fetchArticles(page: number, itemsPerPage: number) {
  const bearerToken = cookies().get("jwtToken")?.value;
  const offset = (page - 1) * itemsPerPage;
  const articlesUrl = `${process.env.API_HOST}/api/articles?offset=${offset}&limit=${itemsPerPage}`;
  const response = await fetch(articlesUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (response.ok) {
    // const { articles, numArticles } = await response.json();
    const { articles, articles_count: numArticles } = await response.json();
    return { articles, numArticles };
  }
  // TODO: error handling
  return { articles: [], numArticles: 0 };
}
