import { useMutation } from "@apollo/client/react";

import { convertToErrorType, getAPIStatusFromMutation, type APIStatus } from "../../../constants/apiConstants";
import {
  DeleteTaskDocument,
  type DeleteTaskMutation,
  type DeleteTaskMutationVariables,
} from "./operation.generated";
import { useResponseHandler, type DeleteTaskCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends DeleteTaskCallbacks {
  ids: string[];
  onRequestFailed?: (error: Error) => void;
}

interface UseDeleteTaskReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useDeleteTask = (): UseDeleteTaskReturnType => {
  const [deleteTask, { data, loading, error }] = useMutation<
    DeleteTaskMutation,
    DeleteTaskMutationVariables
  >(DeleteTaskDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { ids, onRequestFailed, ...callbacks } = args;
    deleteTask({
      variables: { ids },
      onCompleted: (responseData) => {
        if (responseData?.deleteTask === undefined || responseData.deleteTask === null) {
          onRequestFailed?.(new Error("The request did not complete. Nothing was deleted."));
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

export default useDeleteTask;
