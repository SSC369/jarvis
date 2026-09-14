import type { GetMeQuery } from "./operation.generated";

export interface GetMeCallbacks {
  onMeLoaded?: (args: {
    id: string;
    email: string;
    username: string | null;
    avatarUrl: string | null;
  }) => void;
}

interface UseResponseHandlerArgs extends GetMeCallbacks {
  data: GetMeQuery | null | undefined;
}

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, onMeLoaded } = args;
    if (!data?.me) return;
    onMeLoaded?.({
      id: data.me.id,
      email: data.me.email,
      username: data.me.username,
      avatarUrl: data.me.avatarUrl,
    });
  };

  return { handleResponse };
};
