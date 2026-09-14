import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { StoreProvider } from "@/stores/StoreProvider";
import CommandCenterController from "./CommandCenterController";

const { mockUseOnlineStatus, mockTriggerSubmitCapture } = vi.hoisted(() => ({
  mockUseOnlineStatus: vi.fn(),
  mockTriggerSubmitCapture: vi.fn(),
}));

vi.mock("@/hooks/useOnlineStatus", () => ({
  useOnlineStatus: () => mockUseOnlineStatus(),
}));

vi.mock("@/api/mutations/SubmitCapture/useSubmitCapture", () => ({
  default: () => ({ triggerAPI: mockTriggerSubmitCapture, apiStatus: 0, apiError: null }),
}));

vi.mock("@/api/mutations/AnswerPendingCapture/useAnswerPendingCapture", () => ({
  default: () => ({ triggerAPI: vi.fn(), apiStatus: 0, apiError: null }),
}));

vi.mock("@/api/mutations/DiscardPendingCapture/useDiscardPendingCapture", () => ({
  default: () => ({ triggerAPI: vi.fn(), apiStatus: 0, apiError: null }),
}));

const renderWithProviders = () =>
  render(
    <StoreProvider>
      <CommandCenterController />
    </StoreProvider>,
  );

describe("CommandCenterController offline behaviour", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("T-3.4: disables the input and shows the offline note while offline", () => {
    mockUseOnlineStatus.mockReturnValue(false);

    renderWithProviders();

    const input = screen.getByPlaceholderText("You're offline");
    expect(input).toBeDisabled();
  });

  it("T-3.4: never dispatches submitCapture while offline, even if Enter fires", () => {
    mockUseOnlineStatus.mockReturnValue(false);

    renderWithProviders();
    const input = screen.getByPlaceholderText("You're offline");
    input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true }));

    expect(mockTriggerSubmitCapture).not.toHaveBeenCalled();
  });

  it("enables the input again once back online", () => {
    mockUseOnlineStatus.mockReturnValue(true);

    renderWithProviders();

    const input = screen.getByPlaceholderText("Type / to begin");
    expect(input).not.toBeDisabled();
  });
});
