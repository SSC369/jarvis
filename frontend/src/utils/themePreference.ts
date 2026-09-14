// A plain client preference, not server state, so it lives outside the MobX
// stores (frontend/CLAUDE.md rule 1 / repo-rules.md §7 reserve stores for
// data the server sent). Persisted to localStorage and applied as a
// `data-theme` attribute on `<html>`; `index.html`'s inline script mirrors
// this module's storage key and values to apply the choice before first
// paint, so a change to either must be mirrored in the other.
export type ThemePreferenceType = "SYSTEM" | "LIGHT" | "DARK";

export const THEME_PREFERENCE_STORAGE_KEY = "slashit:theme-preference";

const isThemePreferenceType = (value: string | null): value is ThemePreferenceType =>
  value === "SYSTEM" || value === "LIGHT" || value === "DARK";

export const getThemePreference = (): ThemePreferenceType => {
  try {
    const stored = localStorage.getItem(THEME_PREFERENCE_STORAGE_KEY);
    return isThemePreferenceType(stored) ? stored : "SYSTEM";
  } catch {
    return "SYSTEM";
  }
};

const applyThemePreference = (preference: ThemePreferenceType): void => {
  const root = document.documentElement;
  if (preference === "LIGHT") {
    root.setAttribute("data-theme", "light");
  } else if (preference === "DARK") {
    root.setAttribute("data-theme", "dark");
  } else {
    root.removeAttribute("data-theme");
  }
};

export const setThemePreference = (preference: ThemePreferenceType): void => {
  try {
    localStorage.setItem(THEME_PREFERENCE_STORAGE_KEY, preference);
  } catch {
    // Private mode or storage disabled: the choice just won't survive a
    // reload. Still apply it for the current page life.
  }
  applyThemePreference(preference);
};
