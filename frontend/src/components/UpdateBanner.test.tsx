import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const { mockUseUpdateAvailable } = vi.hoisted(() => ({
  mockUseUpdateAvailable: vi.fn(),
}));

vi.mock("../hooks/useUpdateAvailable", () => ({
  useUpdateAvailable: () => mockUseUpdateAvailable(),
}));

import UpdateBanner from "./UpdateBanner";

describe("UpdateBanner", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("T-3.5: renders nothing when no update is available", () => {
    mockUseUpdateAvailable.mockReturnValue({
      updateAvailable: false,
      applyUpdate: vi.fn(),
    });

    const { container } = render(<UpdateBanner />);

    expect(container).toBeEmptyDOMElement();
  });

  it("T-3.5: renders and calls applyUpdate on click when an update is available", () => {
    const applyUpdate = vi.fn();
    mockUseUpdateAvailable.mockReturnValue({ updateAvailable: true, applyUpdate });

    render(<UpdateBanner />);
    fireEvent.click(screen.getByRole("button", { name: "Reload to update" }));

    expect(applyUpdate).toHaveBeenCalledTimes(1);
  });
});
