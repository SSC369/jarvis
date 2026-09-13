/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../../../types.generated';

import { gql } from '@apollo/client';
export type DiscardPendingCaptureMutationVariables = Exact<{
  pendingCaptureId: string | number;
}>;


export type DiscardPendingCaptureMutation = { discardPendingCapture: boolean };


export const DiscardPendingCaptureDocument = gql`
    mutation DiscardPendingCapture($pendingCaptureId: ID!) {
  discardPendingCapture(pendingCaptureId: $pendingCaptureId)
}
    `;