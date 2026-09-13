import { useLazyQuery } from "@apollo/client/react";

import { getAPIStatusFromNetworkStatus, type APIStatus } from "../../../constants/apiConstants";
import {
  GetRecordsDocument,
  type GetRecordsQuery,
  type GetRecordsQueryVariables,
} from "./operation.generated";

interface UseGetRecordsReturnType {
  triggerAPI: (variables: GetRecordsQueryVariables) => void;
  data: GetRecordsQuery | undefined;
  apiStatus: APIStatus;
  apiError: Error | null;
}

/**
 * Apollo Client 4's useLazyQuery has no onCompleted/onError; the caller
 * reacts to `data` (typically in a useEffect) and passes it to this
 * operation's responseHandler itself. See repo-rules.md §6.2.
 */
const useGetRecords = (): UseGetRecordsReturnType => {
  const [getRecords, { data, networkStatus, error }] = useLazyQuery<
    GetRecordsQuery,
    GetRecordsQueryVariables
  >(GetRecordsDocument, {
    fetchPolicy: "network-only",
    notifyOnNetworkStatusChange: true,
  });

  const triggerAPI = (variables: GetRecordsQueryVariables): void => {
    getRecords({ variables });
  };

  return {
    triggerAPI,
    data,
    apiStatus: getAPIStatusFromNetworkStatus(networkStatus, data),
    apiError: error instanceof Error ? error : null,
  };
};

export default useGetRecords;
