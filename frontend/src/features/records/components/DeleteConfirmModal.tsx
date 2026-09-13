import { TrashIcon } from "lucide-react";
import type { ReactElement } from "react";

import Button from "../../../design-system/components/Button";
import * as Styles from "./styles";

interface DeleteConfirmModalProps {
  taskTitle: string | null;
  count: number;
  onCancel: () => void;
  onConfirm: () => void;
}

const DeleteConfirmModal = (props: DeleteConfirmModalProps): ReactElement => {
  const { taskTitle, count, onCancel, onConfirm } = props;
  const isSingle = count <= 1 && taskTitle !== null;

  return (
    <div className={Styles.modalOverlayStyles}>
      <div className={Styles.modalStyles}>
        <div className={Styles.modalBodyStyles}>
          <TrashIcon size={22} className="shrink-0 text-destructive" />
          <div>
            <div className={Styles.modalTitleStyles}>
              Delete {isSingle ? "this task" : `${count} tasks`}?
            </div>
            <div className={Styles.modalMessageStyles}>
              {isSingle ? (
                <>
                  <span className={Styles.modalTaskNameStyles}>{taskTitle}</span> will be
                  removed from your records. This cannot be undone.
                </>
              ) : (
                <>{count} tasks will be removed from your records. This cannot be undone.</>
              )}
            </div>
          </div>
        </div>
        <div className={Styles.modalActionsStyles}>
          <Button onClick={onCancel}>Cancel</Button>
          <Button variant="danger" onClick={onConfirm}>
            Delete {isSingle ? "task" : "tasks"}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;
