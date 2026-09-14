const SHORT_DATE_FORMAT = new Intl.DateTimeFormat(undefined, {
  weekday: "short",
  day: "numeric",
  month: "short",
});

const LONG_DATE_FORMAT = new Intl.DateTimeFormat(undefined, {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const LONG_DATE_ONLY_FORMAT = new Intl.DateTimeFormat(undefined, {
  day: "numeric",
  month: "long",
  year: "numeric",
});

const TIME_ONLY_FORMAT = new Intl.DateTimeFormat(undefined, {
  hour: "numeric",
  minute: "2-digit",
});

export const formatShortDate = (value: string | null): string => {
  if (value === null) return "No due date";
  return SHORT_DATE_FORMAT.format(new Date(value));
};

export const formatLongDate = (value: string | null): string => {
  if (value === null) return "No due date";
  return LONG_DATE_FORMAT.format(new Date(value));
};

export const formatLongDateTime = (value: string): string => {
  const date = new Date(value);
  return `${LONG_DATE_ONLY_FORMAT.format(date)} at ${TIME_ONLY_FORMAT.format(date)}`;
};

const MINUTE_MS = 60_000;
const HOUR_MS = 60 * MINUTE_MS;
const DAY_MS = 24 * HOUR_MS;

/** "just now", "5m ago", "3h ago", "2d ago", falling back to a long date
 * past a week. Used by capture history, per design §4's "relative time". */
export const formatRelativeTime = (value: string): string => {
  const elapsedMs = Date.now() - new Date(value).getTime();
  if (elapsedMs < MINUTE_MS) return "just now";
  if (elapsedMs < HOUR_MS) return `${Math.floor(elapsedMs / MINUTE_MS)}m ago`;
  if (elapsedMs < DAY_MS) return `${Math.floor(elapsedMs / HOUR_MS)}h ago`;
  if (elapsedMs < 7 * DAY_MS) return `${Math.floor(elapsedMs / DAY_MS)}d ago`;
  return formatLongDate(value);
};
