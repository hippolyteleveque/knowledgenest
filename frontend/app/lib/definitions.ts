export type Article = {
  id: string;
  url: string;
  description: string;
  imageUrl: string;
  title: string;
};

export type ChatMessage = {
  id?: string;
  message: string;
  chatConversationId?: string;
  type: string;
};

export type ChatConversation = {
  id: string;
  name: string;
  created_at: Date;
};
