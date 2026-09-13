import type { TaskFieldsFragment } from "../../../fragments/TaskFields.generated";
import type { GetTasksQuery } from "./operation.generated";

export interface GetTasksCallbacks {
  onTasksLoaded?: (tasks: TaskFieldsFragment[]) => void;
}

interface UseResponseHandlerArgs extends GetTasksCallbacks {
  data: GetTasksQuery | null | undefined;
}

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, onTasksLoaded } = args;
    if (!data?.tasks) return;
    onTasksLoaded?.(data.tasks);
  };

  return { handleResponse };
};
