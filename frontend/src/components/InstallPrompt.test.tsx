import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import InstallPrompt from "./InstallPrompt";

const fireBeforeInstallPrompt = (): void => {
  act(() => {
    const event = new Event("beforeinstallprompt", { cancelable: true }) as Event & {
      prompt: () => Promise<void>;
    };
    event.prompt = async () => {};
    window.dispatchEvent(event);
  });
};

const fireAppInstalled = (): void => {
  act(() => {
    window.dispatchEvent(new Event("appinstalled"));
  });
};

describe("InstallPrompt", () => {
  beforeEach(() => {
    window.sessionStorage.clear();
  });

  afterEach(() => {
    window.sessionStorage.clear();
  });

  it("T-3.1: renders once beforeinstallprompt fires on first mount", () => {
    render(<InstallPrompt />);
    fireBeforeInstallPrompt();

    expect(screen.getByText("Install Slashit")).toBeInTheDocument();
  });

  it("T-3.1: does not render again after a dismiss, in the same session", () => {
    const { unmount } = render(<InstallPrompt />);
    fireBeforeInstallPrompt();
    fireEvent.click(screen.getByRole("button", { name: "Not now" }));
    expect(screen.queryByText("Install Slashit")).not.toBeInTheDocument();
    unmount();

    render(<InstallPrompt />);
    fireBeforeInstallPrompt();

    expect(screen.queryByText("Install Slashit")).not.toBeInTheDocument();
  });

  it("T-3.2: never renders again after appinstalled fires", () => {
    const { unmount } = render(<InstallPrompt />);
    fireBeforeInstallPrompt();
    expect(screen.getByText("Install Slashit")).toBeInTheDocument();

    fireAppInstalled();
    expect(screen.queryByText("Install Slashit")).not.toBeInTheDocument();
    unmount();

    render(<InstallPrompt />);
    fireBeforeInstallPrompt();

    expect(screen.queryByText("Install Slashit")).not.toBeInTheDocument();
  });
});
