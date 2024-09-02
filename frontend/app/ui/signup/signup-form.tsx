"use client";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { signup } from "@/app/lib/actions";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useFormStatus } from "react-dom";

function SignupButton() {
  const { pending } = useFormStatus();

  return (
    <Button type="submit" className="w-full" disabled={pending}>
      {pending ? "Signing up..." : "Sign Up"}
    </Button>
  );
}

export default function SignupForm() {
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSignup(formData: FormData) {
    setError("");
    const result = await signup(formData);
    if (result.error) {
      setError(result.error);
    } else if (result.success) {
      router.push("/login");
    }
  }

  return (
    <form className="grid gap-4" action={handleSignup}>
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
        </div>
        <Input id="password" type="password" name="password" required />
      </div>
      <SignupButton />
    </form>
  );
}
