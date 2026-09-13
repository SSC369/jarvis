/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import * as Types from '../../../../types.generated';

import { gql } from '@apollo/client';
export type UpdateTimezoneInput = {
  timezone: string;
};

export type UpdateTimezoneMutationVariables = Exact<{
  input: Types.UpdateTimezoneInput;
}>;


export type UpdateTimezoneMutation = { updateTimezone:
    | { __typename: 'InvalidTimezone', message: string }
    | { __typename: 'Settings', timezone: string, updatedAt: string }
   };


export const UpdateTimezoneDocument = gql`
    mutation UpdateTimezone($input: UpdateTimezoneInput!) {
  updateTimezone(input: $input) {
    __typename
    ... on Settings {
      timezone
      updatedAt
    }
    ... on InvalidTimezone {
      message
    }
  }
}
    `;