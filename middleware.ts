import { NextRequest, NextResponse } from "next/server";
// import { decrypt } from '@/app/lib/session'
import { cookies } from "next/headers";

// 1. Specify protected and public routes
const protectedRoutes = ["/app", "/app/chat", "/app/settings"];
const publicRoutes = ["/login", "/signup", "/"];

export default async function middleware(req: NextRequest) {
  // 2. Check if the current route is protected or public
  let isVerified = false;
  const path = req.nextUrl.pathname;
  const isProtectedRoute = protectedRoutes.includes(path);
  const isPublicRoute = publicRoutes.includes(path);

  // 3. Decrypt the session from the cookie
  const cookie = cookies().get("jwtToken")?.value;
  // Call backend to verify that the cookie is correct
  if (cookie) {
    const verifyRequest = await fetch("http://localhost:3000/api/auth/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: cookie }),
    });
    isVerified = verifyRequest.ok;
  }

  // 5. Redirect to /login if the user is not authenticated
  if (isProtectedRoute && !isVerified) {
    return NextResponse.redirect(new URL("/login", req.nextUrl));
  }

  // 6. Redirect to /dashboard if the user is authenticated
  if (isPublicRoute && isVerified && !req.nextUrl.pathname.startsWith("/app")) {
    return NextResponse.redirect(new URL("/app", req.nextUrl));
  }

  return NextResponse.next();
}

// Routes Middleware should not run on
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
