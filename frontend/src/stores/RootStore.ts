import { CaptureStoreModel } from "./CaptureStore";
import { RecordsStoreModel } from "./RecordsStore";
import { SettingsStoreModel } from "./SettingsStore";

export class RootStore {
  capture = CaptureStoreModel.create();
  records = RecordsStoreModel.create();
  settings = SettingsStoreModel.create();

  clear(): void {
    this.capture.clear();
    this.records.clear();
    this.settings.clear();
  }
}
