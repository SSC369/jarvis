import { ListIcon } from "lucide-react";
import type { ReactElement } from "react";

import Button from "../../../design-system/components/Button";
import * as Styles from "./styles";

interface EmptyRecordsProps {
  onStartCapturing: () => void;
}

const EmptyRecords = (props: EmptyRecordsProps): ReactElement => {
  const { onStartCapturing } = props;

  return (
    <div className={Styles.emptyContainerStyles}>
      <div className={Styles.emptyIconStyles}>
        <ListIcon size={24} />
      </div>
      <div className={Styles.emptyTitleStyles}>Nothing recorded yet</div>
      <div className={Styles.emptyBodyStyles}>
        Records appear here the moment you capture one. Nothing is hidden from this view.
      </div>
      <div className={Styles.emptyActionStyles}>
        <Button variant="primary" onClick={onStartCapturing}>
          Start capturing
        </Button>
      </div>
    </div>
  );
};

export default EmptyRecords;
