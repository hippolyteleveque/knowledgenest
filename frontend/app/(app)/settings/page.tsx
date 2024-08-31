import SettingsForm from "@/app/ui/settings/settings-form";
import { getMyUser } from "@/app/lib/data";

export default async function Page() {
  const user = await getMyUser();
  const {
    setting: { ai_provider: aiProvider },
  } = user;

  return (
    <main className="flex flex-1 flex-col pt-5 px-4">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <SettingsForm aiProvider={aiProvider}/>
    </main>
  );
}
