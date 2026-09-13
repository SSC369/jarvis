import { useMutation } from "@apollo/client/react";

import { convertToErrorType, getAPIStatusFromMutation, type APIStatus } from "../../../constants/apiConstants";
import {
  AnswerPendingCaptureDocument,
  type AnswerPendingCaptureMutation,
  type AnswerPendingCaptureMutationVariables,
} from "./operation.generated";
import { useResponseHandler, type AnswerPendingCaptureCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends AnswerPendingCaptureCallbacks {
  pendingCaptureId: string;
  answer: string;
  /** A top-level failure (network, auth) rather than a typed CaptureResult member. */
  onRequestFailed?: (error: Error) => void;
}

interface UseAnswerPendingCaptureReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useAnswerPendingCapture = (): UseAnswerPendingCaptureReturnType => {
  const [answerPendingCapture, { data, loading, error }] = useMutation<
    AnswerPendingCaptureMutation,
    AnswerPendingCaptureMutationVariables
  >(AnswerPendingCaptureDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { pendingCaptureId, answer, onRequestFailed, ...callbacks } = args;
    answerPendingCapture({
      variables: { pendingCaptureId, answer },
      onCompleted: (responseData) => {
        if (!responseData?.answerPendingCapture) {
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

export default useAnswerPendingCapture;
