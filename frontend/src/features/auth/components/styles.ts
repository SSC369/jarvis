// Shared styles for the auth components (AuthCard, OtpInput). One file, like
// every other feature's styles.ts. Values are pixel-matched to
// process-docs/002-authentication/assets/canvas/Main.dc.html and
// VerifyOTP.dc.html. Every colour comes from a tier-2 token in
// design-system/tokens.css; no raw hex anywhere in this file.

// AuthCard: full-page shell -------------------------------------------------

export const pageStyles =
  "relative flex min-h-screen w-full items-center justify-center bg-background " +
  "[background-image:radial-gradient(circle,var(--color-border-strong)_1.2px,transparent_1.2px)] " +
  "[background-size:26px_26px] [background-position:-4px_-4px]";

export const vignetteStyles =
  "pointer-events-none absolute inset-0 " +
  "[background:radial-gradient(ellipse_at_center,transparent_40%,var(--color-background)_92%)]";

export const wrapStyles = "relative z-10 flex w-full items-center justify-center p-10";

export const colStyles = "flex w-[400px] flex-col gap-[22px]";

export const wordmarkStyles = "flex items-center justify-center gap-[9px]";

export const markStyles =
  "flex h-[27px] w-[27px] shrink-0 items-center justify-center rounded-[7px] bg-foreground text-background";

export const wtextStyles = "font-mono text-[19px] font-medium tracking-[-0.015em] text-foreground";

export const wtextDotStyles = "text-command";

export const cardStyles =
  "rounded-xl border border-border bg-card p-8 " +
  "shadow-[0_1px_2px_color-mix(in_srgb,var(--color-foreground)_5%,transparent)]";

export const footerStyles = "text-center text-[13px] text-foreground-secondary";

// OtpInput --------------------------------------------------------------

export const otpRowStyles = "flex justify-center gap-[9px]";

export const otpBoxStyles =
  "h-[56px] w-[46px] rounded-[9px] border border-border-strong bg-card text-center " +
  "font-mono text-[22px] font-medium text-foreground outline-none " +
  "focus:border-accent focus:shadow-[0_0_0_3px_var(--color-accent-wash)] " +
  "disabled:cursor-not-allowed disabled:opacity-60";

export const otpBoxErrorStyles = "border-destructive bg-destructive-wash text-destructive";
