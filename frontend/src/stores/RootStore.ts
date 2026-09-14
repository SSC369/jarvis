import { AuthStoreModel } from "./AuthStore";
import { CaptureStoreModel } from "./CaptureStore";
import { RecordsStoreModel } from "./RecordsStore";
import { SettingsStoreModel } from "./SettingsStore";

export class RootStore {
  auth = AuthStoreModel.create();
  capture = CaptureStoreModel.create();
  records = RecordsStoreModel.create();
  settings = SettingsStoreModel.create();

  clear(): void {
    this.auth.clear();
    this.capture.clear();
    this.records.clear();
    this.settings.clear();
  }
}
