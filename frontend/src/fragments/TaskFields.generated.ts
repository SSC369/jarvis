/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../types.generated';

import { gql } from '@apollo/client';
export type TaskFieldsFragment = { id: string, title: string, dueAt: string | null, status: string, isOverdue: boolean, origin: string, originalInput: string | null, createdAt: string, updatedAt: string };

export const TaskFieldsFragmentDoc = gql`
    fragment TaskFields on Task {
  id
  title
  dueAt
  status
  isOverdue
  origin
  originalInput
  createdAt
  updatedAt
}
    `;