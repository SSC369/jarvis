import { makeAutoObservable } from "mobx";

export class AuthStoreModel {
  id: string | null = null;
  email: string | null = null;
  username: string | null = null;
  avatarUrl: string | null = null;

  constructor() {
    makeAutoObservable(this, {}, { autoBind: true });
  }

  setMe(me: {
    id: string;
    email: string;
    username: string | null;
    avatarUrl: string | null;
  }): void {
    this.id = me.id;
    this.email = me.email;
    this.username = me.username;
    this.avatarUrl = me.avatarUrl;
  }

  clear(): void {
    this.id = null;
    this.email = null;
    this.username = null;
    this.avatarUrl = null;
  }

  static create(): AuthStoreModel {
    return new AuthStoreModel();
  }
}
