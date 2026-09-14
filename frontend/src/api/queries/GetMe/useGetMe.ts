import { useLazyQuery } from "@apollo/client/react";

import { getAPIStatusFromNetworkStatus, type APIStatus } from "../../../constants/apiConstants";
import { GetMeDocument, type GetMeQuery, type GetMeQueryVariables } from "./operation.generated";

interface UseGetMeReturnType {
  triggerAPI: () => void;
  data: GetMeQuery | undefined;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useGetMe = (): UseGetMeReturnType => {
  const [getMe, { data, networkStatus, error }] = useLazyQuery<GetMeQuery, GetMeQueryVariables>(
    GetMeDocument,
    {
      fetchPolicy: "network-only",
      notifyOnNetworkStatusChange: true,
    },
  );

  const triggerAPI = (): void => {
    getMe();
  };

  return {
    triggerAPI,
    data,
    apiStatus: getAPIStatusFromNetworkStatus(networkStatus, data),
    apiError: error instanceof Error ? error : null,
  };
};

export default useGetMe;
