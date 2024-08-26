export async function fetchSources(conversationId: string, bearerToken: string) {
    const sourcesUrl = `${process.env.NEXT_PUBLIC_API_HOST}/api/v1/chat/${conversationId}/sources`;
    const response = await fetch(sourcesUrl, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${bearerToken}`,
      },
    });
    if (response.ok) {
      // const { articles, numArticles } = await response.json();
      const sources = await response.json();
      return sources;
    }
    // TODO: error handling
    return {};
  }