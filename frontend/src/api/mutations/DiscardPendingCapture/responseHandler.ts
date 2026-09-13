import type { DiscardPendingCaptureMutation } from "./operation.generated";

export interface DiscardPendingCaptureCallbacks {
  onDiscarded?: () => void;
}

interface UseResponseHandlerArgs extends DiscardPendingCaptureCallbacks {
  data: DiscardPendingCaptureMutation | null | undefined;
}

export const useResponseHandler = (): { handleResponse: (args: UseResponseHandlerArgs) => void } => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, onDiscarded } = args;
    if (data?.discardPendingCapture) {
      onDiscarded?.();
    }
  };

  return { handleResponse };
};
