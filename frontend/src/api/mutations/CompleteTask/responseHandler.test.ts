import { describe, expect, it, vi } from "vitest";

import { useResponseHandler } from "./responseHandler";
import type { CompleteTaskMutation } from "./operation.generated";

const baseTask = {
  __typename: "Task" as const,
  id: "1",
  title: "Finish API docs",
  dueAt: null,
  status: "done",
  isOverdue: false,
  origin: "command",
  originalInput: null,
  createdAt: "2026-09-13T00:00:00Z",
  updatedAt: "2026-09-13T00:00:00Z",
};

describe("CompleteTask responseHandler", () => {
  it("calls onTaskCompleted for a Task result", () => {
    const { handleResponse } = useResponseHandler();
    const onTaskCompleted = vi.fn();
    const data: CompleteTaskMutation = { completeTask: baseTask };

    handleResponse({ data, onTaskCompleted });

    expect(onTaskCompleted).toHaveBeenCalledWith(baseTask);
  });

  it("calls onNoFieldsToUpdate for a NoFieldsToUpdate result", () => {
    const { handleResponse } = useResponseHandler();
    const onNoFieldsToUpdate = vi.fn();
    const data: CompleteTaskMutation = {
      completeTask: { __typename: "NoFieldsToUpdate", message: "Nothing was supplied to change" },
    };

    handleResponse({ data, onNoFieldsToUpdate });

    expect(onNoFieldsToUpdate).toHaveBeenCalledWith("Nothing was supplied to change");
  });

  it("calls onRecordNotFound for a RecordNotFound result", () => {
    const { handleResponse } = useResponseHandler();
    const onRecordNotFound = vi.fn();
    const data: CompleteTaskMutation = {
      completeTask: { __typename: "RecordNotFound", message: "No record with that id belongs to you" },
    };

    handleResponse({ data, onRecordNotFound });

    expect(onRecordNotFound).toHaveBeenCalledWith("No record with that id belongs to you");
  });

  it("throws via assertNever for an unhandled typename", () => {
    const { handleResponse } = useResponseHandler();
    const data = {
      completeTask: { __typename: "SomethingNew" },
    } as unknown as CompleteTaskMutation;

    expect(() => handleResponse({ data })).toThrow(/Unhandled UpdateTaskResult type/);
  });
});
