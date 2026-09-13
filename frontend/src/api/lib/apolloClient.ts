import { ApolloClient } from "@apollo/client";

import { cache } from "./cache";
import { link } from "./links";

export const apolloClient = new ApolloClient({
  link,
  cache,
  defaultOptions: {
    watchQuery: { errorPolicy: "all" },
    query: { errorPolicy: "all" },
    mutate: { errorPolicy: "all" },
  },
});
