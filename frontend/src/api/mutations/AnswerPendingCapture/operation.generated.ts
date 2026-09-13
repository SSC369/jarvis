/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../../../types.generated';

import { gql } from '@apollo/client';
import { TaskFieldsFragmentDoc } from '../../../fragments/TaskFields.generated';
export type AnswerPendingCaptureMutationVariables = Exact<{
  pendingCaptureId: string | number;
  answer: string;
}>;


export type AnswerPendingCaptureMutation = { answerPendingCapture:
    | { __typename: 'MalformedResult', message: string, reason: string }
    | { __typename: 'NonCommandGuidance', originalInput: string }
    | { __typename: 'PendingQuestionCreated', pendingCaptureId: string, question: string }
    | { __typename: 'ProviderTimeout', message: string, budgetSeconds: number }
    | { __typename: 'ProviderUnavailable', message: string }
    | { __typename: 'SharedQuotaExhausted', message: string }
    | { __typename: 'TaskCreated', task: { id: string, title: string, dueAt: string | null, status: string, isOverdue: boolean, origin: string, originalInput: string | null, createdAt: string, updatedAt: string } }
    | { __typename: 'TasksListed', tasks: Array<{ id: string, title: string, dueAt: string | null, status: string, isOverdue: boolean, origin: string, originalInput: string | null, createdAt: string, updatedAt: string }> }
    | { __typename: 'UnrecognisedCommand', attemptedName: string, closestMatches: Array<string> }
    | { __typename: 'UserLimitReached', message: string, limit: number, resetsAt: string }
   };


export const AnswerPendingCaptureDocument = gql`
    mutation AnswerPendingCapture($pendingCaptureId: ID!, $answer: String!) {
  answerPendingCapture(pendingCaptureId: $pendingCaptureId, answer: $answer) {
    __typename
    ... on TaskCreated {
      task {
        ...TaskFields
      }
    }
    ... on TasksListed {
      tasks {
        ...TaskFields
      }
    }
    ... on PendingQuestionCreated {
      pendingCaptureId
      question
    }
    ... on NonCommandGuidance {
      originalInput
    }
    ... on UnrecognisedCommand {
      attemptedName
      closestMatches
    }
    ... on UserLimitReached {
      message
      limit
      resetsAt
    }
    ... on ProviderUnavailable {
      message
    }
    ... on ProviderTimeout {
      message
      budgetSeconds
    }
    ... on SharedQuotaExhausted {
      message
    }
    ... on MalformedResult {
      message
      reason
    }
  }
}
    ${TaskFieldsFragmentDoc}`;