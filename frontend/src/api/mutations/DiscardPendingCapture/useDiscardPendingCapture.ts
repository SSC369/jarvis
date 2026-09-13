import { useMutation } from "@apollo/client/react";

import { convertToErrorType, getAPIStatusFromMutation, type APIStatus } from "../../../constants/apiConstants";
import {
  DiscardPendingCaptureDocument,
  type DiscardPendingCaptureMutation,
  type DiscardPendingCaptureMutationVariables,
} from "./operation.generated";
import { useResponseHandler, type DiscardPendingCaptureCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends DiscardPendingCaptureCallbacks {
  pendingCaptureId: string;
}

interface UseDiscardPendingCaptureReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useDiscardPendingCapture = (): UseDiscardPendingCaptureReturnType => {
  const [discardPendingCapture, { data, loading, error }] = useMutation<
    DiscardPendingCaptureMutation,
    DiscardPendingCaptureMutationVariables
  >(DiscardPendingCaptureDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { pendingCaptureId, ...callbacks } = args;
    discardPendingCapture({
      variables: { pendingCaptureId },
      onCompleted: (responseData) => {
        handleResponse({ data: responseData, ...callbacks });
      },
    });
  };

  return {
    triggerAPI,
    apiStatus: getAPIStatusFromMutation(loading, data, error),
    apiError: convertToErrorType(error),
  };
};

export default useDiscardPendingCapture;
