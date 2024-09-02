import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Form from "@/app/ui/signup/signup-form";

export default function Page() {
  return (
    <div className="flex items-center justify-content h-screen w-full">
      <Card className="mx-auto max-w-sm w-96">
        <CardHeader>
          <CardTitle className="text-2xl">Sign Up</CardTitle>
          <CardDescription>Enter your email below to signup</CardDescription>
        </CardHeader>
        <CardContent>
          <Form />
        </CardContent>
      </Card>
    </div>
  );
}
