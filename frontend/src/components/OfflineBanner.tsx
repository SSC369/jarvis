import { WifiOff } from "lucide-react";
import type { ReactElement } from "react";

import { useOnlineStatus } from "../hooks/useOnlineStatus";
import * as Styles from "./styles";

/** FR-40: renders while `navigator.onLine` is false. The Capture input reads
 * the same hook directly to disable submit; this banner is the ambient
 * notice shown across every route. */
export const OfflineBanner = (): ReactElement | null => {
  const isOnline = useOnlineStatus();
  if (isOnline) return null;

  return (
    <div className={`${Styles.bannerBaseStyles} ${Styles.offlineBannerStyles}`}>
      <WifiOff size={16} />
      <span className={Styles.bannerTextStyles}>
        You're offline. Records already loaded still work; capturing is paused
        until you're back online.
      </span>
    </div>
  );
};

export default OfflineBanner;
