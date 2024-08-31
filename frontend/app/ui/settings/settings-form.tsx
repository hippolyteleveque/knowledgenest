"use client";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { updateSettings } from "@/app/lib/actions";
import { useState, FormEvent } from "react";

import KnBanner from "../common/banner";

const AI_PROVIDERS = [
  { value: "openai", label: "OpenAI" },
  { value: "anthropic", label: "Anthropic" },
  { value: "mistral", label: "MistralAI" },
];

type SettingsFormProps = {
  aiProvider: string;
};

export default function SettingsForm(props: SettingsFormProps) {
  const [state, setState] = useState({ message: "", success: true });
  const [showBanner, setShowBanner] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const result = await updateSettings(formData);
    setState((prevState) => ({ ...prevState, ...result }));
    setShowBanner(true);
    setTimeout(() => setShowBanner(false), 3000);
  };

  return (
    <>
      {showBanner && <KnBanner message={state.message} />}
      <form onSubmit={handleSubmit} className="space-y-4 max-w-xs">
        <div className="max-w-[200px]">
          <label
            htmlFor="ai-provider"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            AI Provider
          </label>
          <Select name="aiProvider" defaultValue={props.aiProvider}>
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
    </>
  );
}
