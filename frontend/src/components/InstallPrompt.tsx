import { Download, X } from "lucide-react";
import { useEffect, useState, type ReactElement } from "react";

import Button from "../design-system/components/Button";
import * as Styles from "./styles";

const DISMISSED_KEY = "slashit-install-prompt-dismissed";

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
}

const wasDismissedThisSession = (): boolean => {
  try {
    return window.sessionStorage.getItem(DISMISSED_KEY) === "true";
  } catch {
    return false;
  }
};

const markDismissedThisSession = (): void => {
  try {
    window.sessionStorage.setItem(DISMISSED_KEY, "true");
  } catch {
    // Private browsing or storage disabled: the prompt may reappear on a
    // later interaction this session, which is the safe failure direction.
  }
};

/** FR-39: shows once per browser session, dismissible, never re-shown after
 * a dismiss or an install. Renders nothing where `beforeinstallprompt`
 * never fires (e.g. iOS Safari) — no fallback UI in V1. */
export const InstallPrompt = (): ReactElement | null => {
  const [deferredEvent, setDeferredEvent] = useState<BeforeInstallPromptEvent | null>(
    null,
  );
  const [dismissed, setDismissed] = useState(wasDismissedThisSession);

  useEffect(() => {
    const handleBeforeInstallPrompt = (event: Event): void => {
      event.preventDefault();
      setDeferredEvent(event as BeforeInstallPromptEvent);
    };
    const handleAppInstalled = (): void => {
      markDismissedThisSession();
      setDismissed(true);
      setDeferredEvent(null);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
    window.addEventListener("appinstalled", handleAppInstalled);
    return () => {
      window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
      window.removeEventListener("appinstalled", handleAppInstalled);
    };
  }, []);

  const handleDismiss = (): void => {
    markDismissedThisSession();
    setDismissed(true);
  };

  const handleInstall = (): void => {
    if (!deferredEvent) return;
    void deferredEvent.prompt();
    markDismissedThisSession();
    setDismissed(true);
  };

  if (dismissed || !deferredEvent) return null;

  return (
    <div className={Styles.installPromptStyles}>
      <Download size={18} />
      <div className="min-w-0 flex-1">
        <div className={Styles.installPromptTitleStyles}>Install Slashit</div>
        <div className={Styles.installPromptBodyStyles}>
          Add it to your home screen for a faster, full-screen way in.
        </div>
        <div className={Styles.installPromptActionsStyles}>
          <Button size="sm" variant="primary" onClick={handleInstall}>
            Install
          </Button>
          <Button size="sm" onClick={handleDismiss}>
            Not now
          </Button>
        </div>
      </div>
      <button
        type="button"
        aria-label="Dismiss"
        className="text-foreground-tertiary"
        onClick={handleDismiss}
      >
        <X size={16} />
      </button>
    </div>
  );
};

export default InstallPrompt;
