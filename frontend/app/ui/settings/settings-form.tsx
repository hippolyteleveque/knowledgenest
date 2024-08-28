import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { updateSettings } from "@/app/lib/actions";
import { getMyUser } from "@/app/lib/data";

const AI_PROVIDERS = [
  { value: "openai", label: "OpenAI" },
  { value: "anthropic", label: "Anthropic" },
  { value: "mistral", label: "MistralAI" },
];

export default async function SettingsForm() {
  const user = await getMyUser();
  const {
    setting: { ai_provider: aiProvider },
  } = user;

  return (
    <form action={updateSettings} className="space-y-4 max-w-xs">
      <div className="max-w-[200px]">
        <label
          htmlFor="ai-provider"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          AI Provider
        </label>
        <Select name="aiProvider" defaultValue={aiProvider}>
          <SelectTrigger>
            <SelectValue placeholder="Select AI Provider" />
          </SelectTrigger>
          <SelectContent>
            {AI_PROVIDERS.map((provider) => (
              <SelectItem key={provider.value} value={provider.value}>
                {provider.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <Button type="submit">Save Settings</Button>
    </form>
  );
}
