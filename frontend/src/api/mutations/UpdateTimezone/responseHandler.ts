import type { UpdateTimezoneMutation } from "./operation.generated";

export interface UpdateTimezoneCallbacks {
  onTimezoneUpdated?: (args: { timezone: string; updatedAt: string }) => void;
  onInvalidTimezone?: (message: string) => void;
}

interface UseResponseHandlerArgs extends UpdateTimezoneCallbacks {
  data: UpdateTimezoneMutation | null | undefined;
}

const assertNever = (value: never): never => {
  throw new Error(`Unhandled UpdateTimezoneResult type: ${JSON.stringify(value)}`);
};

export const useResponseHandler = (): {
  handleResponse: (args: UseResponseHandlerArgs) => void;
} => {
  const handleResponse = (args: UseResponseHandlerArgs): void => {
    const { data, ...callbacks } = args;
    if (!data?.updateTimezone) return;

    const result = data.updateTimezone;
    switch (result.__typename) {
      case "Settings":
        callbacks.onTimezoneUpdated?.({
          timezone: result.timezone,
          updatedAt: result.updatedAt,
        });
        return;
      case "InvalidTimezone":
        callbacks.onInvalidTimezone?.(result.message);
        return;
      default:
        assertNever(result);
    }
  };

  return { handleResponse };
};
