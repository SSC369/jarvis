import { useLazyQuery } from "@apollo/client/react";

import { getAPIStatusFromNetworkStatus, type APIStatus } from "../../../constants/apiConstants";
import {
  GetCaptureHistoryDocument,
  type GetCaptureHistoryQuery,
  type GetCaptureHistoryQueryVariables,
} from "./operation.generated";

interface UseGetCaptureHistoryReturnType {
  triggerAPI: (variables: GetCaptureHistoryQueryVariables) => void;
  data: GetCaptureHistoryQuery | undefined;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useGetCaptureHistory = (): UseGetCaptureHistoryReturnType => {
  const [getCaptureHistory, { data, networkStatus, error }] = useLazyQuery<
    GetCaptureHistoryQuery,
    GetCaptureHistoryQueryVariables
  >(GetCaptureHistoryDocument, {
    fetchPolicy: "network-only",
    notifyOnNetworkStatusChange: true,
  });

  const triggerAPI = (variables: GetCaptureHistoryQueryVariables): void => {
    getCaptureHistory({ variables });
  };

  return {
    triggerAPI,
    data,
    apiStatus: getAPIStatusFromNetworkStatus(networkStatus, data),
    apiError: error instanceof Error ? error : null,
  };
};

export default useGetCaptureHistory;
