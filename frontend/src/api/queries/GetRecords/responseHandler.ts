import type { TaskFieldsFragment } from "../../../fragments/TaskFields.generated";
import type { GetRecordsQuery } from "./operation.generated";

export interface GetRecordsCallbacks {
  onRecordsLoaded?: (records: TaskFieldsFragment[]) => void;
}

interface UseResponseHandlerArgs extends GetRecordsCallbacks {
  data: GetRecordsQuery | null | undefined;
}

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, onRecordsLoaded } = args;
    if (!data?.records) return;
    onRecordsLoaded?.(data.records);
  };

  return { handleResponse };
};
