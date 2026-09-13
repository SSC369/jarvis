import { describe, expect, it, vi } from "vitest";

import { useResponseHandler } from "./responseHandler";
import type { DeleteTaskMutation } from "./operation.generated";

describe("DeleteTask responseHandler", () => {
  it("calls onDeleted with the count, including zero", () => {
    const { handleResponse } = useResponseHandler();
    const onDeleted = vi.fn();

    handleResponse({ data: { deleteTask: 2 } as DeleteTaskMutation, onDeleted });
    expect(onDeleted).toHaveBeenCalledWith(2);

    onDeleted.mockClear();
    handleResponse({ data: { deleteTask: 0 } as DeleteTaskMutation, onDeleted });
    expect(onDeleted).toHaveBeenCalledWith(0);
  });

  it("does nothing when data is absent", () => {
    const { handleResponse } = useResponseHandler();
    expect(() => handleResponse({ data: null })).not.toThrow();
  });
});
