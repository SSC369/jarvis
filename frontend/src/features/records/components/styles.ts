// Records pane (shared by RecordsController / RecordDetailController)
export const paneStyles = "flex-1 overflow-y-auto px-10 py-7";

// Toolbar: tabs + search + sort
export const toolbarStyles = "mb-[18px] flex items-center justify-between";
export const tabsStyles = "flex gap-1.5";
export const tabStyles =
  "flex h-8 items-center rounded-md border border-transparent px-3.5 text-[13px] font-medium text-foreground-secondary";
export const tabOnStyles = "border-border-strong bg-card text-foreground";
export const toolbarRightStyles = "flex gap-2.5";
export const searchBoxStyles =
  "flex h-9 w-[280px] items-center gap-2.5 rounded-md border border-border-strong bg-card px-3 text-[13.5px] text-foreground-tertiary";
export const searchInputStyles = "w-full border-0 bg-transparent text-foreground outline-none placeholder:text-foreground-tertiary";

// Table
export const cardStyles = "overflow-hidden rounded-lg border border-border bg-card";
export const tableStyles = "w-full border-collapse bg-card";
export const theadRowStyles = "border-b border-border-strong bg-background";
export const thStyles = "px-4 py-2.5 text-left text-[11px] font-semibold uppercase tracking-[0.07em] text-foreground-tertiary";
export const rowStyles = "cursor-pointer border-b border-border last:border-b-0 hover:bg-background";
export const tdStyles = "h-[52px] px-4 align-middle text-sm";
export const typeTagStyles = "inline-flex items-center gap-1.5 text-[12.5px] text-foreground-secondary";
export const typeDotStyles = "h-1.5 w-1.5 shrink-0 rounded-sm bg-command";
export const titleCellStyles = "font-medium text-foreground";
export const titleDoneCellStyles = "font-medium text-foreground-tertiary";
export const dateCellStyles = "text-foreground-secondary";
export const cardFootStyles =
  "flex items-center justify-between border-t border-border bg-background px-4 py-2.5 text-xs text-foreground-tertiary";

export const pillBaseStyles = "inline-flex h-[23px] items-center gap-1.5 rounded-full border px-2.5 text-[11.5px] font-medium";
export const pillPendingStyles = "border-command-wash bg-command-wash text-command";
export const pillDoneStyles = "border-success-wash bg-success-wash text-success";

// Empty state
export const emptyContainerStyles = "flex flex-1 flex-col items-center justify-center px-10 text-center";
export const emptyIconStyles =
  "mx-auto mb-[18px] flex h-[52px] w-[52px] items-center justify-center rounded-xl bg-background text-foreground-tertiary";
export const emptyTitleStyles = "text-[19px] font-semibold text-foreground";
export const emptyBodyStyles = "mt-2 max-w-[420px] text-sm text-foreground-secondary";
export const emptyActionStyles = "mt-5";

// Detail
export const breadcrumbStyles = "mb-5 flex items-center gap-2 text-[13px] text-foreground-tertiary";
export const breadcrumbCurrentStyles = "text-foreground";
export const detailTitleStyles = "font-serif text-[32px] leading-[1.2] text-foreground";
export const detailFieldsStyles = "mt-[22px]";
export const detailRowStyles = "flex border-b border-border py-3.5";
export const detailLabelStyles = "w-[150px] pt-0.5 text-[11px] font-semibold uppercase tracking-[0.07em] text-foreground-tertiary";
export const detailValueStyles = "flex-1 text-[14.5px] text-foreground";
export const detailInputBlockStyles = "mt-[22px]";
export const detailInputEchoStyles =
  "mt-2 rounded-lg border border-border bg-background px-3.5 py-3 font-mono text-[13.5px] text-foreground";
export const detailActionsRowStyles = "mt-[26px] flex gap-2.5";

// Edit form
export const formRowStyles = "mb-[18px] flex flex-col gap-1.5";
export const formLabelStyles = "text-[11px] font-semibold uppercase tracking-[0.07em] text-foreground-tertiary";
export const controlStyles =
  "flex h-[42px] items-center rounded-md border border-border-strong bg-card px-3.5 text-sm text-foreground";
export const controlInputStyles = "w-full border-0 bg-transparent text-[17px] text-foreground outline-none";
export const controlReadOnlyStyles = "text-foreground-secondary";
export const segStyles = "flex w-fit overflow-hidden rounded-md border border-border-strong";
export const segOptionStyles =
  "flex h-10 cursor-pointer items-center px-4 text-[13.5px] font-medium text-foreground-secondary";
export const segOptionOnStyles = "bg-accent text-white";
export const noteInfoStyles = "mt-1.5 flex gap-2.5 rounded-[10px] border border-accent-wash bg-accent-wash px-4 py-3.5";
export const noteInfoTextStyles = "text-[13.5px] text-foreground";
export const formActionsRowStyles = "mt-6 flex gap-2.5";

// Delete confirm modal
export const modalOverlayStyles = "fixed inset-0 z-10 flex items-center justify-center bg-black/30";
export const modalStyles = "w-[460px] overflow-hidden rounded-xl bg-card shadow-2xl";
export const modalBodyStyles = "flex gap-3 p-6 pb-5";
export const modalTitleStyles = "text-[17px] font-semibold text-foreground";
export const modalMessageStyles = "mt-1.5 text-[13.5px] text-foreground-secondary";
export const modalTaskNameStyles = "font-mono text-foreground";
export const modalActionsStyles = "flex justify-end gap-2.5 border-t border-border bg-background px-6 py-3.5";
