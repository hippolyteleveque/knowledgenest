"use server";

import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { z } from "zod";
import { revalidatePath } from "next/cache";

const AuthSchema = z.object({
  email: z.string(),
  password: z.string(),
});

export async function signup(formData: FormData) {
  const validatedFields = AuthSchema.parse({
    email: formData.get("email"),
    password: formData.get("password"),
  });
  const { email, password } = validatedFields;
  const signupUrl = `${process.env.API_HOST}/api/auth/signup`;
  const response = await fetch(signupUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  // TODO wait for the response to get finish properly and handle errors
  redirect("/login");
}

export async function login(formData: FormData) {
  const validatedFields = AuthSchema.parse({
    email: formData.get("email"),
    password: formData.get("password"),
  });
  const { email, password } = validatedFields;
  const authForm = new FormData();
  authForm.append("username", email);
  authForm.append("password", password);
  const loginUrl = `${process.env.API_HOST}/api/auth/login`;
  const response = await fetch(loginUrl, {
    method: "POST",
    body: authForm,
  });

  if (response.ok) {
    const { access_token } = await response.json();
    cookies().set("jwtToken", access_token, {
      httpOnly: true,
      secure: true,
      sameSite: "lax",
      path: "/",
    });
    redirect("/app");
  }
}

const ArticleSchema = z.object({
  articleUrl: z.string(),
});

export async function addArticle(formData: FormData) {
  const validatedFields = ArticleSchema.parse({
    articleUrl: formData.get("articleUrl"),
  });
  const { articleUrl } = validatedFields;
  const addArticleUrl = `${process.env.API_HOST}/api/articles/`;
  const bearerToken = cookies().get("jwtToken")?.value;
  // TODO : clean up this abomination
  if (!bearerToken) {
    redirect("/login");
  }
  const response = await fetch(addArticleUrl, {
    method: "POST",
    body: JSON.stringify({ url: articleUrl }),
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (!response.ok) {
    // TODO put some error message
  }
  revalidatePath("/app");
}

export async function deleteArticle(articleId: number) {
  const bearerToken = cookies().get("jwtToken")?.value;
  // TODO : clean up this abomination
  if (!bearerToken) {
    redirect("/login");
  }
  const deletionUrl = `${process.env.API_HOST}/api/articles/${articleId}`;
  const response = await fetch(deletionUrl, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${bearerToken}`,
    },
  });
  if (!response.ok) {
    // TODO put some error handling logic
  }
  revalidatePath("/app");
}

export async function sendChatMessage(message: string, conversationId: string) {
  const bearerToken = cookies().get("jwtToken")?.value;
  // // TODO : clean up this abomination
  if (!bearerToken) {
    redirect("/login");
  }
  let chatUrl = `${process.env.API_HOST}/api/chat/`;
  if (conversationId) {
    chatUrl += conversationId.toString();
  }
  const response = await fetch(chatUrl, {
    method: "POST",
    body: JSON.stringify({ message }),
    headers: {
      Authorization: `Bearer ${bearerToken}`,
      "Content-Type": "application/json",
    },
  });
  const resp = await response.json();
  revalidatePath("/app/chat");
  return resp.message;
}

export async function startConversation(message: string) {
  const bearerToken = cookies().get("jwtToken")?.value;
  // // TODO : clean up this abomination
  if (!bearerToken) {
    redirect("/login");
  }
  const chatUrl = `${process.env.API_HOST}/api/chat/`;
  const response = await fetch(chatUrl, {
    method: "POST",
    body: JSON.stringify({ message }),
    headers: {
      Authorization: `Bearer ${bearerToken}`,
      "Content-Type": "application/json",
    },
  });
  const resp = await response.json();
  revalidatePath("/app/chat");
  return { message: resp.message, conversationId: resp.conversation_id };
}
