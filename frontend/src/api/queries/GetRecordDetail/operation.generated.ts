/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../../../types.generated';

import { gql } from '@apollo/client';
import { TaskFieldsFragmentDoc } from '../../../fragments/TaskFields.generated';
export type GetRecordDetailQueryVariables = Exact<{
  id: string | number;
}>;


export type GetRecordDetailQuery = { record:
    | { __typename: 'RecordNotFound', message: string }
    | { __typename: 'Task', id: string, title: string, dueAt: string | null, status: string, isOverdue: boolean, origin: string, originalInput: string | null, createdAt: string, updatedAt: string }
   };


export const GetRecordDetailDocument = gql`
    query GetRecordDetail($id: ID!) {
  record(id: $id) {
    __typename
    ... on Task {
      ...TaskFields
    }
    ... on RecordNotFound {
      message
    }
  }
}
    ${TaskFieldsFragmentDoc}`;