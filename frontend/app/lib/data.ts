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

export async function fetchConversations() {
  const conversationsUrl = `${process.env.API_HOST}/api/chat`;
  const response = await fetch(conversationsUrl, {
    method: "GET",
  });
  if (response.ok) {
    // const { articles, numArticles } = await response.json();
    const conversations = await response.json();
    return conversations;
  }
  // TODO: error handling
  return { conversations: [] };
}

export async function fetchConversation(id: string) {
  const conversationUrl = `${process.env.API_HOST}/api/chat/${id}`;
  const response = await fetch(conversationUrl, {
    method: "GET",
  });
  if (response.ok) {
    // const { articles, numArticles } = await response.json();
    const conversation = await response.json();
    return conversation;
  }
  // TODO: error handling
  return [];
}
