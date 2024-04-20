import { cookies } from "next/headers";

export async function fetchArticles() {
  const bearerToken = cookies().get("jwtToken")?.value;
  const articlesUrl = `${process.env.API_HOST}/api/articles`;
  const response = await fetch(articlesUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (response.ok) {
    const fetchedArticles = await response.json();
    return fetchedArticles;
  }
  // TODO: error handling
  return [];
}
