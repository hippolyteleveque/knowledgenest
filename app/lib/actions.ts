"use server";

import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { headers } from 'next/headers'
import { z } from "zod";

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
  const host = headers().get('x-forwarded-host')
  const signupUrl = `http://${host}/api/auth/signup`
  const response = await fetch(signupUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

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
  const host = headers().get('x-forwarded-host')
  const loginUrl = `http://${host}/api/auth/login`
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
