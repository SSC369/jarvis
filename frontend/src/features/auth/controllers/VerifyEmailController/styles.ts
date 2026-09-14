// Card-content styles for VerifyEmailController. AuthCard/OtpInput's own
// shell styles live in features/auth/components/styles.ts; these are the
// styles specific to this screen's content. Pixel-matched to
// process-docs/002-authentication/assets/canvas/VerifyOTP.dc.html. Every
// colour is a tier-2 token from design-system/tokens.css, no raw hex.

export const titleStyles =
  "m-0 mb-1.5 text-center font-serif text-[26px] font-normal tracking-[-0.005em] text-foreground";

export const subtitleStyles =
  "m-0 mb-[26px] text-center text-[13.5px] leading-normal text-foreground-secondary";

export const emailStyles = "font-mono";

export const noteErrorStyles =
  "mb-[18px] flex gap-2.5 rounded-[10px] border border-destructive-wash bg-destructive-wash px-[15px] py-[13px] text-[13px] leading-normal text-destructive";

export const noteIconStyles = "mt-px shrink-0";

export const resendRowStyles =
  "mb-[22px] flex justify-center text-[12.5px] text-foreground-tertiary";

export const resendLinkStyles =
  "cursor-pointer border-0 bg-transparent p-0 font-sans text-[12.5px] text-accent underline-offset-2 hover:underline disabled:cursor-not-allowed";

export const verifyButtonStyles = "w-full justify-center";

export const spinnerStyles =
  "h-[15px] w-[15px] animate-spin rounded-full border-2 border-white/40 border-t-white";

export const centerMsgStyles = "text-center";

export const checkCircleStyles =
  "mx-auto mb-3.5 flex h-[52px] w-[52px] items-center justify-center rounded-full bg-success-wash text-success";

export const amberWarnStyles =
  "mx-auto mb-3.5 flex h-[52px] w-[52px] items-center justify-center rounded-full bg-command-wash text-command";

export const confirmSubtitleStyles = "text-center text-[13.5px] leading-normal text-foreground-secondary";

export const footerLinkStyles = "text-accent hover:text-accent";
