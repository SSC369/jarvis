import type { ReactElement } from "react";

import { cn } from "../../../utils/cn";
import type { CaptureCommand } from "../../../constants/captureCommands";
import * as Styles from "./styles";

interface CommandPaletteProps {
  matches: CaptureCommand[];
  selectedIndex: number;
  countLabel: string;
  onPick: (name: string) => void;
}

const CommandPalette = (props: CommandPaletteProps): ReactElement => {
  const { matches, selectedIndex, countLabel, onPick } = props;

  return (
    <div className={Styles.paletteStyles}>
      <div className={Styles.paletteTopStyles}>
        <span className="text-[11px] font-semibold uppercase tracking-[0.07em] text-foreground-tertiary">
          Commands
        </span>
        <span className="text-[11.5px] text-foreground-tertiary">{countLabel}</span>
      </div>
      {matches.map((command, index) => (
        <div
          key={command.name}
          className={cn(Styles.commandRowStyles, index === selectedIndex && Styles.commandRowSelectedStyles)}
          onClick={() => onPick(command.name)}
        >
          <div className={Styles.commandNameStyles}>{command.name}</div>
          <div className="text-[13px] text-foreground-secondary">{command.description}</div>
        </div>
      ))}
      <div className={Styles.paletteFootStyles}>
        <span>
          <span className={Styles.kbdStyles}>↑↓</span> move
        </span>
        <span>
          <span className={Styles.kbdStyles}>⏎</span> choose
        </span>
        <span>
          <span className={Styles.kbdStyles}>Esc</span> dismiss
        </span>
      </div>
    </div>
  );
};

export default CommandPalette;
