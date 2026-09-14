import type { ReactElement } from "react";

import { cn } from "../utils/cn";
import * as Styles from "./styles";

interface InlineSpinnerProps {
  size?: number;
  className?: string;
}

/** A small spinner for a control's own in-flight state (§4 of the design's
 * "Saving" sub-state note), distinct from a full-surface loading skeleton. */
export const InlineSpinner = (props: InlineSpinnerProps): ReactElement => {
  const { size = 14, className } = props;
  return (
    <span
      role="status"
      aria-label="Saving"
      className={cn(Styles.inlineSpinnerStyles, className)}
      style={{ width: size, height: size }}
    />
  );
};

export default InlineSpinner;
