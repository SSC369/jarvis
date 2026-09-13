import { useMutation } from "@apollo/client/react";

import { convertToErrorType, getAPIStatusFromMutation, type APIStatus } from "../../../constants/apiConstants";
import {
  UpdateTimezoneDocument,
  type UpdateTimezoneMutation,
  type UpdateTimezoneMutationVariables,
} from "./operation.generated";
import { useResponseHandler, type UpdateTimezoneCallbacks } from "./responseHandler";

interface TriggerAPIArgs extends UpdateTimezoneCallbacks {
  timezone: string;
  onRequestFailed?: (error: Error) => void;
}

interface UseUpdateTimezoneReturnType {
  triggerAPI: (args: TriggerAPIArgs) => void;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useUpdateTimezone = (): UseUpdateTimezoneReturnType => {
  const [updateTimezone, { data, loading, error }] = useMutation<
    UpdateTimezoneMutation,
    UpdateTimezoneMutationVariables
  >(UpdateTimezoneDocument);

  const { handleResponse } = useResponseHandler();

  const triggerAPI = (args: TriggerAPIArgs): void => {
    const { timezone, onRequestFailed, ...callbacks } = args;
    updateTimezone({
      variables: { input: { timezone } },
      onCompleted: (responseData) => {
        if (!responseData?.updateTimezone) {
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

export default useUpdateTimezone;
