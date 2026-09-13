import { InfoIcon } from "lucide-react";
import type { ChangeEvent, ReactElement } from "react";

import Button from "../../../design-system/components/Button";
import { cn } from "../../../utils/cn";
import { formatLongDate } from "../utils/formatDate";
import * as Styles from "./styles";

export type EditableStatus = "PENDING" | "DONE";

interface RecordEditFormProps {
  title: string;
  dueAt: string | null;
  status: EditableStatus;
  onTitleChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onStatusChange: (status: EditableStatus) => void;
  onSave: () => void;
  onCancel: () => void;
}

const RecordEditForm = (props: RecordEditFormProps): ReactElement => {
  const { title, dueAt, status, onTitleChange, onStatusChange, onSave, onCancel } = props;

  return (
    <div>
      <div className={Styles.formRowStyles}>
        <span className={Styles.formLabelStyles}>Task</span>
        <div className={Styles.controlStyles}>
          <input
            className={Styles.controlInputStyles}
            type="text"
            value={title}
            onChange={onTitleChange}
            autoFocus
          />
        </div>
      </div>
      <div className={Styles.formRowStyles}>
        <span className={Styles.formLabelStyles}>Due</span>
        <div className={cn(Styles.controlStyles, Styles.controlReadOnlyStyles)}>
          {formatLongDate(dueAt)}
        </div>
      </div>
      <div className={Styles.formRowStyles}>
        <span className={Styles.formLabelStyles}>Status</span>
        <div className={Styles.segStyles}>
          <div
            className={cn(
              Styles.segOptionStyles,
              status === "PENDING" && Styles.segOptionOnStyles,
            )}
            onClick={() => onStatusChange("PENDING")}
          >
            Pending
          </div>
          <div
            className={cn(Styles.segOptionStyles, status === "DONE" && Styles.segOptionOnStyles)}
            onClick={() => onStatusChange("DONE")}
          >
            Done
          </div>
        </div>
      </div>
      <div className={Styles.noteInfoStyles}>
        <InfoIcon size={17} className="shrink-0 text-accent" />
        <div className={Styles.noteInfoTextStyles}>
          The date you were given when this was captured stays as it is unless you change it
          here.
        </div>
      </div>
      <div className={Styles.formActionsRowStyles}>
        <Button variant="primary" onClick={onSave}>
          Save changes
        </Button>
        <Button onClick={onCancel}>Cancel</Button>
      </div>
    </div>
  );
};

export default RecordEditForm;
