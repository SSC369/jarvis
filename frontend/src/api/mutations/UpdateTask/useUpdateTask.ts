import { useMutation } from "@apollo/client/react";

import { convertToErrorType, getAPIStatusFromMutation, type APIStatus } from "../../../constants/apiConstants";
import {
  UpdateTaskDocument,
  type UpdateTaskMutation,
  type UpdateTaskMutationVariables,
} from "./operation.generated";
import { useResponseHandler, type UpdateTaskCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends UpdateTaskCallbacks {
  id: string;
  title?: string | null;
  status?: "PENDING" | "DONE" | null;
  dueAt?: string | null;
  onRequestFailed?: (error: Error) => void;
}

interface UseUpdateTaskReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useUpdateTask = (): UseUpdateTaskReturnType => {
  const [updateTask, { data, loading, error }] = useMutation<
    UpdateTaskMutation,
    UpdateTaskMutationVariables
  >(UpdateTaskDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { id, title, status, dueAt, onRequestFailed, ...callbacks } = args;
    updateTask({
      variables: { id, input: { title, status, dueAt } },
      onCompleted: (responseData) => {
        if (!responseData?.updateTask) {
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

export default useUpdateTask;
