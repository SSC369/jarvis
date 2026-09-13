import type { ReactElement } from "react";

import Button from "../../../design-system/components/Button";
import { CAPTURE_COMMANDS } from "../../../constants/captureCommands";
import * as Styles from "./styles";

interface EmptyStateProps {
  onFillCommand: (name: string) => void;
}

const EmptyState = (props: EmptyStateProps): ReactElement => {
  const { onFillCommand } = props;

  return (
    <div className={Styles.emptyContainerStyles}>
      <div className={Styles.emptyColumnStyles}>
        <div className={Styles.emptyHeadlineStyles}>Everything starts with a slash.</div>
        <div className={Styles.emptySubheadStyles}>
          Type a command and Slashit records it. Whatever you record, you can find, change
          and delete afterwards.
        </div>
        <div className={Styles.emptySuggestionsRowStyles}>
          {CAPTURE_COMMANDS.map((command) => (
            <Button
              key={command.name}
              size="sm"
              className="font-mono text-command"
              onClick={() => onFillCommand(command.name)}
            >
              {command.name}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EmptyState;
