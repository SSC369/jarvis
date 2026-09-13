import { useMutation } from "@apollo/client/react";

import {
  convertToErrorType,
  getAPIStatusFromMutation,
  type APIStatus,
} from "../../../constants/apiConstants";
import { SubmitCaptureDocument, type SubmitCaptureMutation, type SubmitCaptureMutationVariables } from "./operation.generated";
import { useResponseHandler, type SubmitCaptureCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends SubmitCaptureCallbacks {
  rawInput: string;
  /** A top-level failure (network, auth) rather than a typed CaptureResult member. */
  onRequestFailed?: (error: Error) => void;
}

interface UseSubmitCaptureReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useSubmitCapture = (): UseSubmitCaptureReturnType => {
  const [submitCapture, { data, loading, error }] = useMutation<
    SubmitCaptureMutation,
    SubmitCaptureMutationVariables
  >(SubmitCaptureDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { rawInput, onRequestFailed, ...callbacks } = args;
    submitCapture({
      variables: { rawInput },
      onCompleted: (responseData) => {
        if (!responseData?.submitCapture) {
          onRequestFailed?.(new Error("The request did not complete. Nothing was saved."));
          return;
        }
        handleResponse({ data: responseData, ...callbacks });
      },
      onError: (mutationError) => onRequestFailed?.(mutationError),
    });
  };

  return {
    triggerAPI,
    apiStatus: getAPIStatusFromMutation(loading, data, error),
    apiError: convertToErrorType(error),
  };
};

export default useSubmitCapture;
