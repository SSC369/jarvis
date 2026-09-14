// Sign up screen styles. Pixel-matched to
// process-docs/002-authentication/assets/canvas/Main.dc.html and
// process-docs/002-authentication/02-design.md §4/§8. Every colour is a
// tier-2 token from design-system/tokens.css; no raw hex, except the
// Google button's own brand mark and text colour, which are Google's fixed
// convention rather than a Slashit design choice — see the dev log.

export const titleStyles =
  "m-0 mb-1.5 font-serif text-[26px] font-normal tracking-[-0.005em] text-foreground";
export const subtitleStyles = "mb-[22px] text-[13.5px] leading-normal text-foreground-secondary";

// Google button and divider, above the form -------------------------------

export const googleButtonStyles =
  "mb-[18px] flex h-[44px] w-full items-center justify-center gap-2.5 rounded-md " +
  "border border-border-strong bg-card text-[14px] font-medium text-foreground";

export const dividerStyles = "mb-[18px] flex items-center gap-3 text-xs text-foreground-tertiary";
export const dividerLineStyles = "h-px flex-1 bg-border";

// Error banner --------------------------------------------------------------

export const noteErrorStyles =
  "mb-[18px] flex gap-[11px] rounded-[10px] border border-destructive-wash bg-destructive-wash " +
  "px-[15px] py-[13px] text-[13px] leading-normal text-destructive";
export const noteErrorIconStyles = "mt-0.5 shrink-0";
export const inlineLinkStyles = "underline hover:no-underline";

// Form fields ---------------------------------------------------------------

export const formRowStyles = "mb-4 flex flex-col gap-1.5";
export const lastFormRowStyles = "mb-[22px] flex flex-col gap-1.5";
export const fieldLabelStyles = "text-[12.5px] font-medium text-foreground-secondary";
export const fieldErrorStyles = "text-[12px] text-destructive";

export const controlStyles =
  "h-[42px] w-full rounded-md border border-border-strong bg-card px-3.5 text-sm text-foreground " +
  "outline-none placeholder:text-foreground-tertiary focus:border-accent " +
  "focus:shadow-[0_0_0_3px_var(--color-accent-wash)]";
export const controlErrorStyles = "border-destructive shadow-[0_0_0_3px_var(--color-destructive-wash)]";

// Submit button ---------------------------------------------------------------

export const submitButtonStyles = "h-11 w-full justify-center text-[14px]";
// Design §7: under prefers-reduced-motion the spinner is replaced by the
// static loading text alone, not a frozen spin.
export const spinnerStyles =
  "h-[15px] w-[15px] animate-spin rounded-full border-2 border-white/40 border-t-white " +
  "motion-reduce:hidden";

// Limited / success confirmation cards --------------------------------------

export const centerCardStyles = "text-center";
export const successIconWrapStyles =
  "mx-auto mb-3.5 flex h-[52px] w-[52px] items-center justify-center rounded-full " +
  "bg-success-wash text-success";
export const limitedIconWrapStyles =
  "mx-auto mb-3.5 flex h-[52px] w-[52px] items-center justify-center rounded-full " +
  "bg-command-wash text-command";
export const statusTitleStyles = titleStyles;
export const statusBodyStyles = "text-[13.5px] leading-normal text-foreground-secondary";
