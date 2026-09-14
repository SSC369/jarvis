import { describe, expect, it } from "vitest";

import { fromDateTimeLocalInputValue, toDateTimeLocalInputValue } from "./formatDate";

describe("fromDateTimeLocalInputValue", () => {
  it("converts a complete datetime-local value to an ISO instant", () => {
    expect(fromDateTimeLocalInputValue("2026-09-20T09:00")).toBe(
      new Date("2026-09-20T09:00").toISOString(),
    );
  });

  it("treats an empty value as no due date", () => {
    expect(fromDateTimeLocalInputValue("")).toBeNull();
  });

  it("treats an unparseable in-progress value as no due date rather than throwing", () => {
    // Caught live: a datetime-local input can transiently report a value
    // Date can't parse while the user is still typing.
    expect(fromDateTimeLocalInputValue("dd/02/26090, 00:--")).toBeNull();
  });
});

describe("toDateTimeLocalInputValue", () => {
  it("returns an empty string for no due date", () => {
    expect(toDateTimeLocalInputValue(null)).toBe("");
  });

  it("round-trips through fromDateTimeLocalInputValue", () => {
    const iso = new Date("2026-09-20T09:00").toISOString();
    expect(fromDateTimeLocalInputValue(toDateTimeLocalInputValue(iso))).toBe(iso);
  });
});
