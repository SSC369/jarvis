import { useMutation } from "@apollo/client/react";

import { convertToErrorType, getAPIStatusFromMutation, type APIStatus } from "../../../constants/apiConstants";
import {
  CompleteTaskDocument,
  type CompleteTaskMutation,
  type CompleteTaskMutationVariables,
} from "./operation.generated";
import { useResponseHandler, type CompleteTaskCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends CompleteTaskCallbacks {
  id: string;
  onRequestFailed?: (error: Error) => void;
}

interface UseCompleteTaskReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useCompleteTask = (): UseCompleteTaskReturnType => {
  const [completeTask, { data, loading, error }] = useMutation<
    CompleteTaskMutation,
    CompleteTaskMutationVariables
  >(CompleteTaskDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { id, onRequestFailed, ...callbacks } = args;
    completeTask({
      variables: { id },
      onCompleted: (responseData) => {
        if (!responseData?.completeTask) {
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

export default useCompleteTask;
