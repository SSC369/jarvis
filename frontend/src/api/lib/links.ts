import { ApolloLink, HttpLink } from "@apollo/client";
import { GraphQLWsLink } from "@apollo/client/link/subscriptions";
import { getMainDefinition } from "@apollo/client/utilities";
import { createClient } from "graphql-ws";

import { authLink } from "./authLink";

const httpUrl = import.meta.env.VITE_GRAPHQL_HTTP_URL;
const wsUrl = import.meta.env.VITE_GRAPHQL_WS_URL;

if (!httpUrl || !wsUrl) {
  throw new Error(
    "VITE_GRAPHQL_HTTP_URL and VITE_GRAPHQL_WS_URL must be set. See .env.example.",
  );
}

const httpLink = authLink.concat(new HttpLink({ uri: httpUrl }));

const wsLink = new GraphQLWsLink(
  createClient({
    url: wsUrl,
  }),
);

/**
 * Routes subscriptions to the WebSocket, everything else to HTTP. One
 * client, one auth path. See repo-rules.md §9.
 */
export const link = ApolloLink.split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  httpLink,
);
