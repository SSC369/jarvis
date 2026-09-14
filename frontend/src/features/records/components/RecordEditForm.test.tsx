import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import RecordEditForm from "./RecordEditForm";

const baseProps = {
  title: "Buy milk",
  dueAt: null,
  status: "PENDING" as const,
  onTitleChange: vi.fn(),
  onStatusChange: vi.fn(),
  onSave: vi.fn(),
  onCancel: vi.fn(),
};

describe("RecordEditForm", () => {
  it("T-4.9: disables the title input and both buttons while isSaving", () => {
    render(<RecordEditForm {...baseProps} isSaving />);

    expect(screen.getByDisplayValue("Buy milk")).toBeDisabled();
    expect(screen.getByText("Cancel")).toBeDisabled();
  });

  it("T-4.9: shows a spinner instead of the Save label while isSaving", () => {
    render(<RecordEditForm {...baseProps} isSaving />);

    expect(screen.queryByText("Save changes")).not.toBeInTheDocument();
    expect(screen.getByRole("status", { name: "Saving" })).toBeInTheDocument();
  });

  it("is interactive and shows the Save label when not saving", () => {
    render(<RecordEditForm {...baseProps} />);

    expect(screen.getByDisplayValue("Buy milk")).not.toBeDisabled();
    expect(screen.getByText("Save changes")).toBeInTheDocument();
    expect(screen.queryByRole("status", { name: "Saving" })).not.toBeInTheDocument();
  });
});
