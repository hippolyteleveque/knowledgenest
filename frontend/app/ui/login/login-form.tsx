"use client";
import { login } from "@/app/lib/actions";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useFormStatus } from "react-dom";

function LoginButton() {
  const { pending } = useFormStatus();

  return (
    <Button type="submit" className="w-full" disabled={pending}>
      {pending ? "Logging in..." : "Login"}
    </Button>
  );
}

export default function LoginForm() {
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleLogin(formData: FormData) {
    setError("");
    const result = await login(formData);
    if (result.error) {
      setError(result.error);
    } else if (result.sucess) {
      router.push("/articles");
    }
  }

  return (
    <form className="grid gap-4" action={handleLogin}>
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <div className="grid gap-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          name="email"
          placeholder="m@example.com"
          required
          autoFocus
        />
      </div>
      <div className="grid gap-2">
        <div className="flex items-center">
          <Label htmlFor="password">Password</Label>
          <Link href="#" className="ml-auto inline-block text-sm underline">
            Forgot your password?
          </Link>
        </div>
        <Input id="password" type="password" name="password" required />
      </div>
      <LoginButton />
    </form>
  );
}
