import { Check, Clock, History, Trash2, X } from "lucide-react";
import { useEffect, useState, type ReactElement } from "react";

import useGetCaptureHistory from "../../../api/queries/GetCaptureHistory/useGetCaptureHistory";
import { useResponseHandler } from "../../../api/queries/GetCaptureHistory/responseHandler";
import type { CaptureTurnFieldsFragment } from "../../../fragments/CaptureTurnFields.generated";
import Button from "../../../design-system/components/Button";
import { API_FAILED, API_FETCHING, API_SUCCESS } from "../../../constants/apiConstants";
import { formatRelativeTime } from "../../../utils/formatDate";
import * as Styles from "./styles";

interface HistoryPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const OUTCOME_PILL: Record<
  CaptureTurnFieldsFragment["outcome"],
  { className: string; label: string; icon: ReactElement }
> = {
  TASK_CREATED: { className: Styles.pillDoneStyles, label: "Task created", icon: <Check size={12} /> },
  QUESTION_ASKED: { className: Styles.pillWaitStyles, label: "Question asked", icon: <Clock size={12} /> },
  DISCARDED: { className: Styles.pillMutedStyles, label: "Discarded", icon: <Trash2 size={12} /> },
  REFUSED: { className: Styles.pillErrStyles, label: "Refused", icon: <X size={12} /> },
};

const HistoryRow = (props: { turn: CaptureTurnFieldsFragment }): ReactElement => {
  const { turn } = props;
  const pill = OUTCOME_PILL[turn.outcome];

  return (
    <div className={Styles.historyRowStyles}>
      <div className={Styles.historyRowHeadStyles}>
        <span className={`${Styles.pillBaseStyles} ${pill.className}`}>
          {pill.icon} {pill.label}
        </span>
        <span className={Styles.historyTimeStyles}>{formatRelativeTime(turn.createdAt)}</span>
      </div>
      <div className={Styles.historyInputTextStyles}>{turn.inputText}</div>
      {turn.questionText && (
        <div className={Styles.historyDetailStyles}>Asked: {turn.questionText}</div>
      )}
      {turn.answerText && (
        <div className={Styles.historyDetailStyles}>Answered: {turn.answerText}</div>
      )}
    </div>
  );
};

/** FR-44, FR-45. Read-only: queries directly, no MobX store, since nothing
 * else in the same tab writes back to this data (design's 04.4 addendum,
 * state management section). */
export const HistoryPanel = (props: HistoryPanelProps): ReactElement | null => {
  const { isOpen, onClose } = props;
  const [items, setItems] = useState<CaptureTurnFieldsFragment[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const { triggerAPI, data, apiStatus } = useGetCaptureHistory();
  const { handleResponse } = useResponseHandler();

  useEffect(() => {
    if (!isOpen) return;
    setItems([]);
    setNextCursor(null);
    triggerAPI({ cursor: null });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  useEffect(() => {
    if (!data) return;
    handleResponse({
      data,
      onHistoryLoaded: (loaded, cursor) => {
        setItems((existing) => [...existing, ...loaded]);
        setNextCursor(cursor);
      },
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  if (!isOpen) return null;

  const isInitialLoad = apiStatus === API_FETCHING && items.length === 0;
  const isLoadingMore = apiStatus === API_FETCHING && items.length > 0;
  const hasFailed = apiStatus === API_FAILED;
  const isEmpty = apiStatus === API_SUCCESS && items.length === 0;

  return (
    <>
      <div className={Styles.historyOverlayStyles} onClick={onClose} />
      <div className={Styles.historyPanelStyles}>
        <div className={Styles.historyHeadStyles}>
          <div className={Styles.historyTitleStyles}>History</div>
          <div className={Styles.historyCloseStyles} onClick={onClose}>
            <X size={16} />
          </div>
        </div>
        <div className={Styles.historyBodyStyles}>
          {isInitialLoad &&
            Array.from({ length: 4 }, (_, index) => (
              <div key={index} className={Styles.historySkeletonRowStyles}>
                <div className="h-[11px] w-[40%] animate-pulse rounded bg-border" />
                <div className="mt-2 h-[11px] w-[75%] animate-pulse rounded bg-border" />
              </div>
            ))}

          {hasFailed && (
            <div className={Styles.historyErrorStyles}>
              <span>Couldn't load your history</span>
              <Button size="sm" onClick={() => triggerAPI({ cursor: null })}>
                Retry
              </Button>
            </div>
          )}

          {isEmpty && (
            <div className={Styles.historyEmptyStyles}>
              <History size={28} className="mb-2.5" />
              Nothing captured yet
            </div>
          )}

          {items.map((turn) => (
            <HistoryRow key={turn.id} turn={turn} />
          ))}

          {items.length > 0 && nextCursor && (
            <div className={Styles.historyLoadMoreStyles}>
              <Button
                size="sm"
                disabled={isLoadingMore}
                onClick={() => triggerAPI({ cursor: nextCursor })}
              >
                {isLoadingMore ? "Loading…" : "Load more"}
              </Button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default HistoryPanel;
