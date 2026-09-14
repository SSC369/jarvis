import { useRegisterSW } from "virtual:pwa-register/react";

interface UseUpdateAvailableReturnType {
  updateAvailable: boolean;
  applyUpdate: () => void;
}

/**
 * Wraps vite-plugin-pwa's own hook. `needRefresh` is true once a new
 * service worker is installed and waiting — with registerType: "prompt"
 * (vite.config.ts) it stays waiting until `updateServiceWorker()` is
 * called, which is what FR-41 requires: the user clicks, nothing swaps
 * silently underneath them.
 */
export const useUpdateAvailable = (): UseUpdateAvailableReturnType => {
  const { needRefresh, updateServiceWorker } = useRegisterSW();
  const [updateAvailable] = needRefresh;

  const applyUpdate = (): void => {
    void updateServiceWorker(true);
  };

  return { updateAvailable, applyUpdate };
};
