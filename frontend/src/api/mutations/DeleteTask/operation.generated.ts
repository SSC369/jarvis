/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../../../types.generated';

import { gql } from '@apollo/client';
export type DeleteTaskMutationVariables = Exact<{
  ids: Array<string | number> | string | number;
}>;


export type DeleteTaskMutation = { deleteTask: number };


export const DeleteTaskDocument = gql`
    mutation DeleteTask($ids: [ID!]!) {
  deleteTask(ids: $ids)
}
    `;