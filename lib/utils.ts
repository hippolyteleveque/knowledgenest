import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// TODO : replace protocol and host handling a bit more properly
export const protocol =
  process.env.NODE_ENV == "development" ? "http" : "https";
