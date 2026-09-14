import { History } from "lucide-react";
import { observer } from "mobx-react-lite";
import { useEffect, useRef, useState, type ChangeEvent, type KeyboardEvent, type ReactElement } from "react";

import type { SubmitCaptureCallbacks } from "../../../../api/mutations/SubmitCapture/responseHandler";
import useAnswerPendingCapture from "../../../../api/mutations/AnswerPendingCapture/useAnswerPendingCapture";
import useDiscardPendingCapture from "../../../../api/mutations/DiscardPendingCapture/useDiscardPendingCapture";
import useSubmitCapture from "../../../../api/mutations/SubmitCapture/useSubmitCapture";
import { API_FETCHING } from "../../../../constants/apiConstants";
import { CAPTURE_COMMANDS } from "../../../../constants/captureCommands";
import type { CaptureStoreModel } from "../../../../stores/CaptureStore";
import { useStore } from "../../../../stores/StoreProvider";
import { useOnlineStatus } from "../../../../hooks/useOnlineStatus";
import CommandInputBar from "../../components/CommandInputBar";
import CommandPalette from "../../components/CommandPalette";
import EmptyState from "../../components/EmptyState";
import HistoryPanel from "../../components/HistoryPanel";
import TurnCard from "../../components/TurnCard";
import * as StreamStyles from "../../components/styles";
import * as Styles from "./styles";

const isPaletteOpen = (input: string): boolean => input.startsWith("/") && !input.includes(" ");

const buildCaptureResultCallbacks = (
  captureStore: CaptureStoreModel,
  turnId: string,
): SubmitCaptureCallbacks => ({
  onTaskCreated: (task) => captureStore.resolveTurn(turnId, { status: "taskCreated", task }),
  onTasksListed: (tasks) => captureStore.resolveTurn(turnId, { status: "taskList", tasks }),
  onPendingQuestionCreated: ({ pendingCaptureId, question }) =>
    captureStore.resolveTurn(turnId, { status: "pending", pendingCaptureId, question, answerDraft: "" }),
  onNonCommandGuidance: (originalInput) =>
    captureStore.resolveTurn(turnId, { status: "nonCommand", originalInput }),
  onUnrecognisedCommand: ({ attemptedName, closestMatches }) =>
    captureStore.resolveTurn(turnId, { status: "unrecognisedCommand", attemptedName, closestMatches }),
  onUserLimitReached: ({ message }) => captureStore.resolveTurn(turnId, { status: "refused", message }),
  onProviderUnavailable: (message) => captureStore.resolveTurn(turnId, { status: "refused", message }),
  onProviderTimeout: ({ message }) => captureStore.resolveTurn(turnId, { status: "refused", message }),
  onSharedQuotaExhausted: (message) => captureStore.resolveTurn(turnId, { status: "refused", message }),
  onMalformedResult: ({ message }) => captureStore.resolveTurn(turnId, { status: "refused", message }),
});

const filterCommands = (input: string) => {
  const query = input.slice(1).toLowerCase();
  return CAPTURE_COMMANDS.filter((command) => command.name.slice(1).includes(query));
};

const CommandCenterController = (): ReactElement => {
  const store = useStore();
  const [input, setInput] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [submittingTurnId, setSubmittingTurnId] = useState<string | null>(null);
  const isOnline = useOnlineStatus();

  const { triggerAPI: triggerSubmitCapture } = useSubmitCapture();
  const {
    triggerAPI: triggerAnswerPendingCapture,
    apiStatus: answerApiStatus,
  } = useAnswerPendingCapture();
  const { triggerAPI: triggerDiscardPendingCapture } = useDiscardPendingCapture();

  const paletteOpen = isPaletteOpen(input);
  const matches = paletteOpen ? filterCommands(input) : [];
  const boundedSelectedIndex = Math.min(selectedIndex, Math.max(matches.length - 1, 0));

  const submit = (rawInput: string): void => {
    const text = rawInput.trim();
    if (!text || !isOnline) return;

    const turnId = store.capture.addLoadingTurn(text);
    triggerSubmitCapture({
      rawInput: text,
      ...buildCaptureResultCallbacks(store.capture, turnId),
      onRequestFailed: (requestError) =>
        store.capture.resolveTurn(turnId, { status: "refused", message: requestError.message }),
    });
  };

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setInput(event.target.value);
    setSelectedIndex(0);
  };

  const pickCommand = (name: string): void => {
    setInput(`${name} `);
    setSelectedIndex(0);
  };

  const handleFillCommand = (name: string): void => {
    if (name === "/tasks") {
      submit(name);
      return;
    }
    pickCommand(name);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>): void => {
    if (event.key === "Escape") {
      event.preventDefault();
      setInput("");
      setSelectedIndex(0);
      return;
    }

    if (paletteOpen) {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        if (matches.length) setSelectedIndex((boundedSelectedIndex + 1) % matches.length);
        return;
      }
      if (event.key === "ArrowUp") {
        event.preventDefault();
        if (matches.length) setSelectedIndex((boundedSelectedIndex - 1 + matches.length) % matches.length);
        return;
      }
      if (event.key === "Enter") {
        event.preventDefault();
        if (matches.length) pickCommand(matches[boundedSelectedIndex].name);
        return;
      }
      return;
    }

    if (event.key === "Enter") {
      event.preventDefault();
      submit(input);
      setInput("");
    }
  };

  const handleAnswerDraftChange = (turnId: string, draft: string): void => {
    store.capture.setAnswerDraft(turnId, draft);
  };

  const handleAnswerSubmit = (turnId: string): void => {
    const turn = store.capture.turns.get(turnId);
    if (!turn || turn.status !== "pending") return;
    const answer = turn.answerDraft.trim();
    if (!answer || !isOnline) return;

    setSubmittingTurnId(turnId);
    triggerAnswerPendingCapture({
      pendingCaptureId: turn.pendingCaptureId,
      answer,
      ...buildCaptureResultCallbacks(store.capture, turnId),
      onRequestFailed: (requestError) =>
        store.capture.resolveTurn(turnId, { status: "refused", message: requestError.message }),
    });
  };

  const handleDiscardPending = (turnId: string): void => {
    const turn = store.capture.turns.get(turnId);
    if (!turn || turn.status !== "pending") return;
    triggerDiscardPendingCapture({
      pendingCaptureId: turn.pendingCaptureId,
      onDiscarded: () => store.capture.removeTurn(turnId),
    });
  };

  const handleUseWithAddTask = (originalInput: string): void => {
    setInput(`/add-task ${originalInput} `);
  };

  const handleRetry = (said: string): void => {
    submit(said);
  };

  const turns = store.capture.getAll();
  const showEmpty = turns.length === 0 && !input;
  const streamRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const streamElement = streamRef.current;
    if (!streamElement) return;
    streamElement.scrollTop = streamElement.scrollHeight;
  }, [turns.length]);

  return (
    <div className={Styles.pageStyles}>
      <div className={Styles.topbarStyles}>
        <div className={Styles.topbarTitleStyles}>Capture</div>
        <div className={Styles.historyButtonStyles} onClick={() => setIsHistoryOpen(true)}>
          <History size={17} />
        </div>
      </div>

      <HistoryPanel isOpen={isHistoryOpen} onClose={() => setIsHistoryOpen(false)} />

      {showEmpty ? (
        <EmptyState onFillCommand={handleFillCommand} />
      ) : (
        <div ref={streamRef} className={StreamStyles.streamContainerStyles}>
          <div className={StreamStyles.streamColumnStyles}>
            {turns.map((turn) => (
              <TurnCard
                key={turn.id}
                turn={turn}
                isAnswering={submittingTurnId === turn.id && answerApiStatus === API_FETCHING}
                onAnswerDraftChange={handleAnswerDraftChange}
                onAnswerSubmit={handleAnswerSubmit}
                onDiscardPending={handleDiscardPending}
                onUseWithAddTask={handleUseWithAddTask}
                onRetry={handleRetry}
              />
            ))}
          </div>
        </div>
      )}

      <div className={StreamStyles.dockStyles}>
        <div className={StreamStyles.inputWrapStyles}>
          {paletteOpen && (
            <CommandPalette
              matches={matches}
              selectedIndex={boundedSelectedIndex}
              countLabel={
                input.length > 1
                  ? `${matches.length} of ${CAPTURE_COMMANDS.length} match "${input.slice(1)}"`
                  : `${CAPTURE_COMMANDS.length} available`
              }
              onPick={pickCommand}
            />
          )}
          <CommandInputBar
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            disabled={!isOnline}
          />
        </div>
        <div className={StreamStyles.hintRowStyles}>
          <span>
            <span className={StreamStyles.kbdStyles}>/</span> commands
          </span>
          <span>
            <span className={StreamStyles.kbdStyles}>Enter</span> run
          </span>
          <span>
            <span className={StreamStyles.kbdStyles}>Esc</span> dismiss
          </span>
        </div>
      </div>
    </div>
  );
};

export default observer(CommandCenterController);
