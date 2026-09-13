import type { DeleteTaskMutation } from "./operation.generated";

export interface DeleteTaskCallbacks {
  onDeleted?: (count: number) => void;
}

interface UseResponseHandlerArgs extends DeleteTaskCallbacks {
  data: DeleteTaskMutation | null | undefined;
}

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, onDeleted } = args;
    if (data?.deleteTask === undefined || data.deleteTask === null) return;
    onDeleted?.(data.deleteTask);
  };

  return { handleResponse };
};
