import { InfoIcon } from "lucide-react";
import { observer } from "mobx-react-lite";
import { useEffect, useMemo, useState, type ChangeEvent, type ReactElement } from "react";

import useUpdateTimezone from "../../../../api/mutations/UpdateTimezone/useUpdateTimezone";
import useGetSettings from "../../../../api/queries/GetSettings/useGetSettings";
import { useResponseHandler } from "../../../../api/queries/GetSettings/responseHandler";
import { useStore } from "../../../../stores/StoreProvider";
import { detectTimezone } from "../../../../utils/detectTimezone";
import * as Styles from "./styles";

const listSupportedTimezones = (): string[] => {
  try {
    return Intl.supportedValuesOf("timeZone");
  } catch {
    return [];
  }
};

const SettingsController = (): ReactElement => {
  const store = useStore();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const timezones = useMemo(listSupportedTimezones, []);

  const { triggerAPI: triggerGetSettings, data } = useGetSettings();
  const { handleResponse } = useResponseHandler();
  const { triggerAPI: triggerUpdateTimezone } = useUpdateTimezone();

  useEffect(() => {
    triggerGetSettings({ detectedTimezone: detectTimezone() });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!data) return;
    handleResponse({
      data,
      onSettingsLoaded: (settings) => store.settings.setSettings(settings),
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  const handleTimezoneChange = (event: ChangeEvent<HTMLSelectElement>): void => {
    const timezone = event.target.value;
    triggerUpdateTimezone({
      timezone,
      onTimezoneUpdated: (updated) => {
        store.settings.setSettings(updated);
        setErrorMessage(null);
      },
      onInvalidTimezone: (message) => setErrorMessage(message),
    });
  };

  return (
    <div className={Styles.pageStyles}>
      <div className={Styles.topbarStyles}>
        <div className={Styles.topbarTitleStyles}>Settings</div>
      </div>
      <div className={Styles.paneStyles}>
        <div className={Styles.contentStyles}>
          <div className={Styles.sectionTitleStyles}>Timezone</div>
          <div className={Styles.sectionBodyStyles}>
            Slashit resolves &ldquo;tomorrow&rdquo; and &ldquo;7pm&rdquo; against this.
          </div>
          <div className={Styles.controlWrapStyles}>
            <div className={Styles.formRowStyles}>
              <span className={Styles.formLabelStyles}>Timezone</span>
              <select
                className={Styles.selectControlStyles}
                value={store.settings.timezone ?? ""}
                onChange={handleTimezoneChange}
              >
                {store.settings.timezone && !timezones.includes(store.settings.timezone) && (
                  <option value={store.settings.timezone}>{store.settings.timezone}</option>
                )}
                {timezones.map((timezone) => (
                  <option key={timezone} value={timezone}>
                    {timezone}
                  </option>
                ))}
              </select>
            </div>
            {errorMessage ? (
              <div className={Styles.noteErrorStyles}>
                <InfoIcon size={17} className="shrink-0 text-destructive" />
                <div className={Styles.noteInfoTextStyles}>{errorMessage}</div>
              </div>
            ) : (
              <div className={Styles.noteInfoStyles}>
                <InfoIcon size={17} className="shrink-0 text-accent" />
                <div className={Styles.noteInfoTextStyles}>
                  Detected from your browser. Changing it affects how Slashit reads dates from
                  here on. Dates already recorded stay exactly as they are.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default observer(SettingsController);
