import { makeAutoObservable } from "mobx";

import type { TaskFieldsFragment } from "../fragments/TaskFields.generated";

export type RecordsKindFilter = "ALL" | "TASKS";
export type RecordsSortField = "CREATED_AT" | "DUE_AT";

export class RecordsStoreModel {
  records: Map<string, TaskFieldsFragment> = new Map();
  order: string[] = [];
  kindFilter: RecordsKindFilter = "ALL";
  searchText = "";
  sortField: RecordsSortField = "CREATED_AT";

  constructor() {
    makeAutoObservable(this, {}, { autoBind: true });
  }

  getVisible(): TaskFieldsFragment[] {
    // The server already applies kindFilter/searchText/sortField (the
    // controller passes them to the GetRecords query); this just renders
    // whatever the store currently holds, in the order the server returned.
    return this.order
      .map((id) => this.records.get(id))
      .filter((record): record is TaskFieldsFragment => record !== undefined);
  }

  setRecords(records: TaskFieldsFragment[]): void {
    this.records.clear();
    this.order = [];
    for (const record of records) {
      this.records.set(record.id, record);
      this.order.push(record.id);
    }
  }

  upsert(record: TaskFieldsFragment): void {
    if (!this.records.has(record.id)) {
      this.order.push(record.id);
    }
    this.records.set(record.id, record);
  }

  remove(id: string): void {
    this.records.delete(id);
    this.order = this.order.filter((recordId) => recordId !== id);
  }

  setKindFilter(filter: RecordsKindFilter): void {
    this.kindFilter = filter;
  }

  setSearchText(text: string): void {
    this.searchText = text;
  }

  setSortField(field: RecordsSortField): void {
    this.sortField = field;
  }

  clear(): void {
    this.records.clear();
    this.order = [];
    this.kindFilter = "ALL";
    this.searchText = "";
    this.sortField = "CREATED_AT";
  }

  static create(): RecordsStoreModel {
    return new RecordsStoreModel();
  }
}
