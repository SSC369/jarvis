import type { KeyboardEvent, ChangeEvent, ReactElement } from "react";

import { cn } from "../../../utils/cn";
import * as Styles from "./styles";

interface CommandInputBarProps {
  value: string;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onKeyDown: (event: KeyboardEvent<HTMLInputElement>) => void;
  disabled?: boolean;
}

const CommandInputBar = (props: CommandInputBarProps): ReactElement => {
  const { value, onChange, onKeyDown, disabled = false } = props;

  return (
    <div className={cn(Styles.inputBarStyles, disabled && "opacity-60")}>
      <span className={Styles.slashBadgeStyles}>/</span>
      <input
        className={Styles.rawInputStyles}
        type="text"
        placeholder={disabled ? "You're offline" : "Type / to begin"}
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        disabled={disabled}
        autoFocus
      />
      <span className={Styles.kbdStyles}>Enter</span>
    </div>
  );
};

export default CommandInputBar;
