export const API_INITIAL = 0 as const;
export const API_FETCHING = 100 as const;
export const API_SUCCESS = 200 as const;
export const API_FAILED = 400 as const;
export const API_FETCHING_PAGINATION = 600 as const;

export type APIStatus =
  | typeof API_INITIAL
  | typeof API_FETCHING
  | typeof API_SUCCESS
  | typeof API_FAILED
  | typeof API_FETCHING_PAGINATION;

export const getAPIStatusFromMutation = (
  loading: boolean,
  data: unknown,
  error: unknown,
): APIStatus => {
  if (loading) return API_FETCHING;
  if (error) return API_FAILED;
  if (data) return API_SUCCESS;
  return API_INITIAL;
};

/**
 * Apollo's NetworkStatus numeric values: loading=1, setVariables=2,
 * fetchMore=3, refetch=4, poll=6, ready=7, error=8, streaming=9.
 */
export const getAPIStatusFromNetworkStatus = (
  networkStatus: number,
  data: unknown,
): APIStatus => {
  if (networkStatus === 8) return API_FAILED;
  if (networkStatus === 3) return API_FETCHING_PAGINATION;
  if (networkStatus === 1 || networkStatus === 2 || networkStatus === 4) {
    return API_FETCHING;
  }
  if (data) return API_SUCCESS;
  return API_INITIAL;
};

export const convertToErrorType = (error: unknown): Error | null => {
  if (error instanceof Error) return error;
  return null;
};
