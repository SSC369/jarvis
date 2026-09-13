import { useLazyQuery } from "@apollo/client/react";

import { getAPIStatusFromNetworkStatus, type APIStatus } from "../../../constants/apiConstants";
import {
  GetTasksDocument,
  type GetTasksQuery,
  type GetTasksQueryVariables,
} from "./operation.generated";

interface UseGetTasksReturnType {
  triggerAPI: () => void;
  data: GetTasksQuery | undefined;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useGetTasks = (): UseGetTasksReturnType => {
  const [getTasks, { data, networkStatus, error }] = useLazyQuery<
    GetTasksQuery,
    GetTasksQueryVariables
  >(GetTasksDocument, {
    fetchPolicy: "network-only",
    notifyOnNetworkStatusChange: true,
  });

  const triggerAPI = (): void => {
    getTasks();
  };

  return {
    triggerAPI,
    data,
    apiStatus: getAPIStatusFromNetworkStatus(networkStatus, data),
    apiError: error instanceof Error ? error : null,
  };
};

export default useGetTasks;
