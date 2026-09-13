import type { KeyboardEvent, ChangeEvent, ReactElement } from "react";

import * as Styles from "./styles";

interface CommandInputBarProps {
  value: string;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onKeyDown: (event: KeyboardEvent<HTMLInputElement>) => void;
}

const CommandInputBar = (props: CommandInputBarProps): ReactElement => {
  const { value, onChange, onKeyDown } = props;

  return (
    <div className={Styles.inputBarStyles}>
      <span className={Styles.slashBadgeStyles}>/</span>
      <input
        className={Styles.rawInputStyles}
        type="text"
        placeholder="Type / to begin"
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        autoFocus
      />
      <span className={Styles.kbdStyles}>Enter</span>
    </div>
  );
};

export default CommandInputBar;
