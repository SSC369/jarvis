import type { CaptureTurnFieldsFragment } from "../../../fragments/CaptureTurnFields.generated";
import type { GetCaptureHistoryQuery } from "./operation.generated";

export interface GetCaptureHistoryCallbacks {
  onHistoryLoaded?: (
    items: CaptureTurnFieldsFragment[],
    nextCursor: string | null,
  ) => void;
}

interface UseResponseHandlerArgs extends GetCaptureHistoryCallbacks {
  data: GetCaptureHistoryQuery | null | undefined;
}

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, onHistoryLoaded } = args;
    if (!data?.captureHistory) return;
    onHistoryLoaded?.(data.captureHistory.items, data.captureHistory.nextCursor ?? null);
  };

  return { handleResponse };
};
