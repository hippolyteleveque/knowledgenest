import { cookies } from "next/headers";
import { ChatConversation, ChatMessage } from "./definitions";

export async function fetchArticles(page: number, itemsPerPage: number) {
  const bearerToken = cookies().get("jwtToken")?.value;
  const offset = (page - 1) * itemsPerPage;
  const articlesUrl = `${process.env.API_HOST}/api/v1/articles/?offset=${offset}&limit=${itemsPerPage}`;
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

export async function fetchConversations(): Promise<ChatConversation[]> {
  const bearerToken = cookies().get("jwtToken")?.value;
  const conversationsUrl = `${process.env.API_HOST}/api/v1/chat/`;
  const response = await fetch(conversationsUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (response.ok) {
    let conversations: ChatConversation[] = await response.json();
    return conversations;
  }
  // TODO: error handling
  return [];
}

export async function fetchConversation(id: string): Promise<ChatMessage[]> {
  const bearerToken = cookies().get("jwtToken")?.value;
  const conversationUrl = `${process.env.API_HOST}/api/v1/chat/${id}`;
  const response = await fetch(conversationUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (response.ok) {
    // const { articles, numArticles } = await response.json();
    const conversation = await response.json();
    return conversation;
  }
  // TODO: error handling
  return [];
}

export async function fetchVideos(page: number, itemsPerPage: number) {
  const bearerToken = cookies().get("jwtToken")?.value;
  const offset = (page - 1) * itemsPerPage;
  const videosUrl = `${process.env.API_HOST}/api/v1/videos/?offset=${offset}&limit=${itemsPerPage}`;
  const response = await fetch(videosUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (response.ok) {
    // const { articles, numArticles } = await response.json();
    const { videos, videos_count: numVideos } = await response.json();
    return { videos, numVideos };
  }
  // TODO: error handling
  return { videos: [], numVideos: 0 };
}