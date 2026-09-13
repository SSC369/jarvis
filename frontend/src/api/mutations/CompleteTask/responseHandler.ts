import type { TaskFieldsFragment } from "../../../fragments/TaskFields.generated";
import type { CompleteTaskMutation } from "./operation.generated";

export interface CompleteTaskCallbacks {
  onTaskCompleted?: (task: TaskFieldsFragment) => void;
  onNoFieldsToUpdate?: (message: string) => void;
  onRecordNotFound?: (message: string) => void;
}

interface UseResponseHandlerArgs extends CompleteTaskCallbacks {
  data: CompleteTaskMutation | null | undefined;
}

const assertNever = (value: never): never => {
  throw new Error(`Unhandled UpdateTaskResult type: ${JSON.stringify(value)}`);
};

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, ...callbacks } = args;
    if (!data?.completeTask) return;

    const result = data.completeTask;
    switch (result.__typename) {
      case "Task":
        callbacks.onTaskCompleted?.(result);
        return;
      case "NoFieldsToUpdate":
        callbacks.onNoFieldsToUpdate?.(result.message);
        return;
      case "RecordNotFound":
        callbacks.onRecordNotFound?.(result.message);
        return;
      default:
        assertNever(result);
    }
  };

  return { handleResponse };
};
