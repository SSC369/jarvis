import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { API_FAILED, API_FETCHING, API_INITIAL, API_SUCCESS } from "@/constants/apiConstants";
import HistoryPanel from "./HistoryPanel";

const { mockUseGetCaptureHistory, mockTriggerAPI } = vi.hoisted(() => ({
  mockUseGetCaptureHistory: vi.fn(),
  mockTriggerAPI: vi.fn(),
}));

vi.mock("@/api/queries/GetCaptureHistory/useGetCaptureHistory", () => ({
  default: () => mockUseGetCaptureHistory(),
}));

describe("HistoryPanel", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("T-4.11: renders nothing when closed", () => {
    mockUseGetCaptureHistory.mockReturnValue({
      triggerAPI: mockTriggerAPI,
      data: undefined,
      apiStatus: API_INITIAL,
      apiError: null,
    });

    const { container } = render(<HistoryPanel isOpen={false} onClose={vi.fn()} />);

    expect(container).toBeEmptyDOMElement();
  });

  it("T-4.11: loading state shows skeleton rows before any data arrives", () => {
    mockUseGetCaptureHistory.mockReturnValue({
      triggerAPI: mockTriggerAPI,
      data: undefined,
      apiStatus: API_FETCHING,
      apiError: null,
    });

    render(<HistoryPanel isOpen onClose={vi.fn()} />);

    expect(screen.getByText("History")).toBeInTheDocument();
    expect(screen.queryByText("Nothing captured yet")).not.toBeInTheDocument();
  });

  it("T-4.11: error state shows a retry action", () => {
    mockUseGetCaptureHistory.mockReturnValue({
      triggerAPI: mockTriggerAPI,
      data: undefined,
      apiStatus: API_FAILED,
      apiError: new Error("network down"),
    });

    render(<HistoryPanel isOpen onClose={vi.fn()} />);

    expect(screen.getByText("Couldn't load your history")).toBeInTheDocument();
    screen.getByText("Retry").click();
    expect(mockTriggerAPI).toHaveBeenCalledWith({ cursor: null });
  });

  it("T-4.11: empty state shows once a load succeeds with no turns", () => {
    mockUseGetCaptureHistory.mockReturnValue({
      triggerAPI: mockTriggerAPI,
      data: { captureHistory: { items: [], nextCursor: null } },
      apiStatus: API_SUCCESS,
      apiError: null,
    });

    render(<HistoryPanel isOpen onClose={vi.fn()} />);

    expect(screen.getByText("Nothing captured yet")).toBeInTheDocument();
  });

  it("T-4.11: success state renders a turn's input text and outcome", () => {
    mockUseGetCaptureHistory.mockReturnValue({
      triggerAPI: mockTriggerAPI,
      data: {
        captureHistory: {
          items: [
            {
              id: "turn-1",
              inputText: "/add-task buy milk",
              outcome: "TASK_CREATED",
              resultingTaskId: "task-1",
              resultingPendingCaptureId: null,
              questionText: null,
              answerText: null,
              createdAt: new Date().toISOString(),
            },
          ],
          nextCursor: null,
        },
      },
      apiStatus: API_SUCCESS,
      apiError: null,
    });

    render(<HistoryPanel isOpen onClose={vi.fn()} />);

    expect(screen.getByText("/add-task buy milk")).toBeInTheDocument();
    expect(screen.getByText("Task created")).toBeInTheDocument();
  });
});
