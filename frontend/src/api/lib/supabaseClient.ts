import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;

if (!supabaseUrl || !supabasePublishableKey) {
  throw new Error(
    "VITE_SUPABASE_URL and VITE_SUPABASE_PUBLISHABLE_KEY must be set. See .env.example.",
  );
}

export const supabaseClient = createClient(supabaseUrl, supabasePublishableKey);

if (import.meta.env.DEV) {
  // No sign-in screen exists yet (out of scope for this slice). Exposed only
  // in dev builds so a session can be established from the console while
  // testing the capture flow manually.
  (window as unknown as { __supabaseClient: typeof supabaseClient }).__supabaseClient = supabaseClient;
}
