import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { afterEach, describe, expect, it, vi } from "vitest";

import { API_INITIAL, API_SUCCESS } from "../../../../constants/apiConstants";
import { StoreProvider } from "../../../../stores/StoreProvider";
import RecordsController from "./RecordsController";

const { mockUseGetRecords } = vi.hoisted(() => ({ mockUseGetRecords: vi.fn() }));

vi.mock("../../../../api/queries/GetRecords/useGetRecords", () => ({
  default: () => mockUseGetRecords(),
}));

const renderWithProviders = () =>
  render(
    <MemoryRouter>
      <StoreProvider>
        <RecordsController />
      </StoreProvider>
    </MemoryRouter>,
  );

describe("RecordsController", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("renders the empty state once a load has completed with zero records", () => {
    mockUseGetRecords.mockReturnValue({
      triggerAPI: vi.fn(),
      data: { records: [] },
      apiStatus: API_SUCCESS,
      apiError: null,
    });

    renderWithProviders();

    expect(screen.getByText("Nothing recorded yet")).toBeInTheDocument();
  });

  it("does not render the empty state before the first load completes", () => {
    mockUseGetRecords.mockReturnValue({
      triggerAPI: vi.fn(),
      data: undefined,
      apiStatus: API_INITIAL,
      apiError: null,
    });

    renderWithProviders();

    expect(screen.queryByText("Nothing recorded yet")).not.toBeInTheDocument();
  });

  it("renders the table, not the empty state, once records are loaded", () => {
    mockUseGetRecords.mockReturnValue({
      triggerAPI: vi.fn(),
      data: {
        records: [
          {
            id: "1",
            title: "Finish API docs",
            dueAt: null,
            status: "pending",
            isOverdue: false,
            origin: "command",
            originalInput: null,
            createdAt: "2026-09-13T00:00:00Z",
            updatedAt: "2026-09-13T00:00:00Z",
          },
        ],
      },
      apiStatus: API_SUCCESS,
      apiError: null,
    });

    renderWithProviders();

    expect(screen.queryByText("Nothing recorded yet")).not.toBeInTheDocument();
    expect(screen.getByText("Finish API docs")).toBeInTheDocument();
  });
});
