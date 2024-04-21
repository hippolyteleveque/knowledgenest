import { cookies } from "next/headers";

export async function fetchArticles(page: number, itemsPerPage: number) {
  const bearerToken = cookies().get("jwtToken")?.value;
  const articlesUrl = `${process.env.API_HOST}/api/articles`;
  const response = await fetch(articlesUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (response.ok) {
    // const { articles, numArticles } = await response.json();
    const articles = await response.json();
    return { articles: articles, numArticles: 107 };
  }
  // TODO: error handling
  return { articles: [], numArticles: 0 };
}
