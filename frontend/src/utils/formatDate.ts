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
