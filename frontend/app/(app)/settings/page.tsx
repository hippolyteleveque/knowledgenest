import SettingsForm from "@/app/ui/settings/settings-form";

export default async function Page() {
  return (
    <main className="flex flex-1 flex-col pt-5 px-4">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <SettingsForm />
    </main>
  );
}
