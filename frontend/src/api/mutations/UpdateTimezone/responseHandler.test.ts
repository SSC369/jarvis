import { describe, expect, it, vi } from "vitest";

import { useResponseHandler } from "./responseHandler";
import type { UpdateTimezoneMutation } from "./operation.generated";

describe("UpdateTimezone responseHandler", () => {
  it("calls onTimezoneUpdated for a Settings result", () => {
    const { handleResponse } = useResponseHandler();
    const onTimezoneUpdated = vi.fn();
    const data: UpdateTimezoneMutation = {
      updateTimezone: {
        __typename: "Settings",
        timezone: "Asia/Kolkata",
        updatedAt: "2026-09-13T00:00:00Z",
      },
    };

    handleResponse({ data, onTimezoneUpdated });

    expect(onTimezoneUpdated).toHaveBeenCalledWith({
      timezone: "Asia/Kolkata",
      updatedAt: "2026-09-13T00:00:00Z",
    });
  });

  it("calls onInvalidTimezone for an InvalidTimezone result", () => {
    const { handleResponse } = useResponseHandler();
    const onInvalidTimezone = vi.fn();
    const data: UpdateTimezoneMutation = {
      updateTimezone: { __typename: "InvalidTimezone", message: '"not/a/zone" is not a known timezone' },
    };

    handleResponse({ data, onInvalidTimezone });

    expect(onInvalidTimezone).toHaveBeenCalledWith('"not/a/zone" is not a known timezone');
  });

  it("throws via assertNever for an unhandled typename", () => {
    const { handleResponse } = useResponseHandler();
    const data = {
      updateTimezone: { __typename: "SomethingNew" },
    } as unknown as UpdateTimezoneMutation;

    expect(() => handleResponse({ data })).toThrow(/Unhandled UpdateTimezoneResult type/);
  });
});
