import { useLazyQuery } from "@apollo/client/react";

import { getAPIStatusFromNetworkStatus, type APIStatus } from "../../../constants/apiConstants";
import {
  GetSettingsDocument,
  type GetSettingsQuery,
  type GetSettingsQueryVariables,
} from "./operation.generated";

interface UseGetSettingsReturnType {
  triggerAPI: (variables: GetSettingsQueryVariables) => void;
  data: GetSettingsQuery | undefined;
  apiStatus: APIStatus;
  apiError: Error | null;
}

const useGetSettings = (): UseGetSettingsReturnType => {
  const [getSettings, { data, networkStatus, error }] = useLazyQuery<
    GetSettingsQuery,
    GetSettingsQueryVariables
  >(GetSettingsDocument, {
    fetchPolicy: "network-only",
    notifyOnNetworkStatusChange: true,
  });

  const triggerAPI = (variables: GetSettingsQueryVariables): void => {
    getSettings({ variables });
  };

  return {
    triggerAPI,
    data,
    apiStatus: getAPIStatusFromNetworkStatus(networkStatus, data),
    apiError: error instanceof Error ? error : null,
  };
};

export default useGetSettings;
