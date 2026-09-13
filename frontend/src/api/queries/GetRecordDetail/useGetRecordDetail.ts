import { useLazyQuery } from "@apollo/client/react";

import { getAPIStatusFromNetworkStatus, type APIStatus } from "../../../constants/apiConstants";
import {
  GetRecordDetailDocument,
  type GetRecordDetailQuery,
  type GetRecordDetailQueryVariables,
} from "./operation.generated";

interface UseGetRecordDetailReturnType {
  triggerAPI: (variables: GetRecordDetailQueryVariables) => void;
  data: GetRecordDetailQuery | undefined;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useGetRecordDetail = (): UseGetRecordDetailReturnType => {
  const [getRecordDetail, { data, networkStatus, error }] = useLazyQuery<
    GetRecordDetailQuery,
    GetRecordDetailQueryVariables
  >(GetRecordDetailDocument, {
    fetchPolicy: "network-only",
    notifyOnNetworkStatusChange: true,
  });

  const triggerAPI = (variables: GetRecordDetailQueryVariables): void => {
    getRecordDetail({ variables });
  };

  return {
    triggerAPI,
    data,
    apiStatus: getAPIStatusFromNetworkStatus(networkStatus, data),
    apiError: error instanceof Error ? error : null,
  };
};

export default useGetRecordDetail;
