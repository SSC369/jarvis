import { RefreshCw } from "lucide-react";
import type { ReactElement } from "react";

import Button from "../design-system/components/Button";
import { useUpdateAvailable } from "../hooks/useUpdateAvailable";
import * as Styles from "./styles";

/** FR-41: renders only once a new service worker is installed and waiting.
 * Reloading happens only on the user's click — `applyUpdate` is the only
 * path that calls `updateServiceWorker`. */
export const UpdateBanner = (): ReactElement | null => {
  const { updateAvailable, applyUpdate } = useUpdateAvailable();
  if (!updateAvailable) return null;

  return (
    <div className={`${Styles.bannerBaseStyles} ${Styles.updateBannerStyles}`}>
      <RefreshCw size={16} />
      <span className={Styles.bannerTextStyles}>A new version of Slashit is ready.</span>
      <div className={Styles.bannerActionsStyles}>
        <Button size="sm" variant="primary" onClick={applyUpdate}>
          Reload to update
        </Button>
      </div>
    </div>
  );
};

export default UpdateBanner;
