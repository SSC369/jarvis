import { makeAutoObservable } from "mobx";

export class SettingsStoreModel {
  timezone: string | null = null;

  constructor() {
    makeAutoObservable(this, {}, { autoBind: true });
  }

  setSettings(settings: { timezone: string }): void {
    this.timezone = settings.timezone;
  }

  clear(): void {
    this.timezone = null;
  }

  static create(): SettingsStoreModel {
    return new SettingsStoreModel();
  }
}
