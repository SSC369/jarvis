import type { TaskFieldsFragment } from "../../../fragments/TaskFields.generated";
import type { UpdateTaskMutation } from "./operation.generated";

export interface UpdateTaskCallbacks {
  onTaskUpdated?: (task: TaskFieldsFragment) => void;
  onNoFieldsToUpdate?: (message: string) => void;
  onRecordNotFound?: (message: string) => void;
}

interface UseResponseHandlerArgs extends UpdateTaskCallbacks {
  data: UpdateTaskMutation | null | undefined;
}

const assertNever = (value: never): never => {
  throw new Error(`Unhandled UpdateTaskResult type: ${JSON.stringify(value)}`);
};

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, ...callbacks } = args;
    if (!data?.updateTask) return;

    const result = data.updateTask;
    switch (result.__typename) {
      case "Task":
        callbacks.onTaskUpdated?.(result);
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
