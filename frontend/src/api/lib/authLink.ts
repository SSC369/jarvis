import { setContext } from "@apollo/client/link/context";

import { supabaseClient } from "./supabaseClient";

/**
 * Reads the current Supabase session token per request. No refresh queue:
 * the Supabase SDK owns refresh, this only asks it for the current session.
 */
export const authLink = setContext(async (_operation, { headers }) => {
  const { data } = await supabaseClient.auth.getSession();
  const accessToken = data.session?.access_token ?? null;

  return {
    headers: {
      ...headers,
      ...(accessToken ? { authorization: `Bearer ${accessToken}` } : {}),
    },
  };
});
