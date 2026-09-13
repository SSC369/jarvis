const WEEKDAY_MONTH_DAY_FORMAT = new Intl.DateTimeFormat(undefined, {
  weekday: "short",
  day: "numeric",
  month: "short",
});

export const formatDueDate = (dueAt: string | null): string => {
  if (dueAt === null) return "No due date";
  return WEEKDAY_MONTH_DAY_FORMAT.format(new Date(dueAt));
};
