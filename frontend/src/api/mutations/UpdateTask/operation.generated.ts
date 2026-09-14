/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../../../types.generated';

import { gql } from '@apollo/client';
import { TaskFieldsFragmentDoc } from '../../../fragments/TaskFields.generated';
export type TaskStatus =
  | 'DONE'
  | 'PENDING';

export type UpdateTaskInput = {
  dueAt?: string | null | undefined;
  status?: TaskStatus | null | undefined;
  title?: string | null | undefined;
};

export type UpdateTaskMutationVariables = Exact<{
  id: string | number;
  input: Types.UpdateTaskInput;
}>;


export type UpdateTaskMutation = { updateTask:
    | { __typename: 'NoFieldsToUpdate', message: string }
    | { __typename: 'RecordNotFound', message: string }
    | { __typename: 'Task', id: string, title: string, dueAt: string | null, status: string, isOverdue: boolean, origin: string, originalInput: string | null, createdAt: string, updatedAt: string }
   };


export const UpdateTaskDocument = gql`
    mutation UpdateTask($id: ID!, $input: UpdateTaskInput!) {
  updateTask(id: $id, input: $input) {
    __typename
    ... on Task {
      ...TaskFields
    }
    ... on NoFieldsToUpdate {
      message
    }
    ... on RecordNotFound {
      message
    }
  }
}
    ${TaskFieldsFragmentDoc}`;