"use server";

import { redirect } from "next/navigation";
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
    body: JSON.stringify({ email, password }),
  });

  redirect("/login");
}
