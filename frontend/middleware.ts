import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { headers } from "next/headers";

// 1. Specify protected and public routes
const publicRoutes = ["/login", "/signup", "/"];

export default async function middleware(req: NextRequest) {
  // 2. Check if the current route is protected or public
  let isVerified = false;
  const path = req.nextUrl.pathname;
  const isPublicRoute = publicRoutes.includes(path);

  if (isPublicRoute) {
    return NextResponse.next();
  }
  // 3. Decrypt the session from the cookie
  const cookie = cookies().get("jwtToken")?.value;
  // Call backend to verify that the cookie is correct
  const host = headers().get("x-forwarded-host");
  const verifyUrl = `${process.env.API_HOST}/api/v1/auth/verify`;
  if (cookie) {
    const verifyRequest = await fetch(verifyUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: cookie }),
    });
    isVerified = verifyRequest.ok;
  }

  // 5. Redirect to /login if the user is not authenticated
  if (!isPublicRoute && !isVerified) {
    return NextResponse.redirect(new URL("/login", req.nextUrl));
  }

  return NextResponse.next();
}

// Routes Middleware should not run on
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
