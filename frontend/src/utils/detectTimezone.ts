export const detectTimezone = (): string | null => {
  try {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    return timezone || null;
  } catch {
    return null;
  }
};
