import { ApolloProvider } from "@apollo/client/react";
import type { ReactElement } from "react";
import { RouterProvider } from "react-router";

import { apolloClient } from "../api/lib/apolloClient";
import { StoreProvider } from "../stores/StoreProvider";
import { router } from "./router";

export const Providers = (): ReactElement => {
  return (
    <ApolloProvider client={apolloClient}>
      <StoreProvider>
        <RouterProvider router={router} />
      </StoreProvider>
    </ApolloProvider>
  );
};
