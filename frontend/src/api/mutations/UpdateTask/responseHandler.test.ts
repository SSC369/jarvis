import { describe, expect, it, vi } from "vitest";

import { useResponseHandler } from "./responseHandler";
import type { UpdateTaskMutation } from "./operation.generated";

const baseTask = {
  __typename: "Task" as const,
  id: "1",
  title: "Finish API docs",
  dueAt: null,
  status: "pending",
  isOverdue: false,
  origin: "command",
  originalInput: null,
  createdAt: "2026-09-13T00:00:00Z",
  updatedAt: "2026-09-13T00:00:00Z",
};

describe("UpdateTask responseHandler", () => {
  it("calls onTaskUpdated for a Task result", () => {
    const { handleResponse } = useResponseHandler();
    const onTaskUpdated = vi.fn();
    const data: UpdateTaskMutation = { updateTask: baseTask };

    handleResponse({ data, onTaskUpdated });

    expect(onTaskUpdated).toHaveBeenCalledWith(baseTask);
  });

  it("calls onNoFieldsToUpdate for a NoFieldsToUpdate result", () => {
    const { handleResponse } = useResponseHandler();
    const onNoFieldsToUpdate = vi.fn();
    const data: UpdateTaskMutation = {
      updateTask: { __typename: "NoFieldsToUpdate", message: "Nothing was supplied to change" },
    };

    handleResponse({ data, onNoFieldsToUpdate });

    expect(onNoFieldsToUpdate).toHaveBeenCalledWith("Nothing was supplied to change");
  });

  it("calls onRecordNotFound for a RecordNotFound result", () => {
    const { handleResponse } = useResponseHandler();
    const onRecordNotFound = vi.fn();
    const data: UpdateTaskMutation = {
      updateTask: { __typename: "RecordNotFound", message: "No record with that id belongs to you" },
    };

    handleResponse({ data, onRecordNotFound });

    expect(onRecordNotFound).toHaveBeenCalledWith("No record with that id belongs to you");
  });

  it("does nothing when data is absent", () => {
    const { handleResponse } = useResponseHandler();
    expect(() => handleResponse({ data: null })).not.toThrow();
    expect(() => handleResponse({ data: undefined })).not.toThrow();
  });

  it("throws via assertNever for an unhandled typename", () => {
    const { handleResponse } = useResponseHandler();
    const data = {
      updateTask: { __typename: "SomethingNew" },
    } as unknown as UpdateTaskMutation;

    expect(() => handleResponse({ data })).toThrow(/Unhandled UpdateTaskResult type/);
  });
});
