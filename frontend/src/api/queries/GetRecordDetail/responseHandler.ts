import type { TaskFieldsFragment } from "../../../fragments/TaskFields.generated";
import type { GetRecordDetailQuery } from "./operation.generated";

export interface GetRecordDetailCallbacks {
  onRecordLoaded?: (task: TaskFieldsFragment) => void;
  onRecordNotFound?: (message: string) => void;
}

interface UseResponseHandlerArgs extends GetRecordDetailCallbacks {
  data: GetRecordDetailQuery | null | undefined;
}

const assertNever = (value: never): never => {
  throw new Error(`Unhandled RecordResult type: ${JSON.stringify(value)}`);
};

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, ...callbacks } = args;
    if (!data?.record) return;

    const result = data.record;
    switch (result.__typename) {
      case "Task":
        callbacks.onRecordLoaded?.(result);
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
