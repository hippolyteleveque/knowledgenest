"use server";

import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { z } from "zod";

const AuthSchema = z.object({
  email: z.string(),
  password: z.string(),
});

export async function signup(formData: FormData) {
  const validatedFields = AuthSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
  });
  const { email, password } = validatedFields.data;
  const response = await fetch("http://localhost:3000/api/auth/signup", {
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
  const response = await fetch("http://localhost:3000/api/auth/login", {
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
