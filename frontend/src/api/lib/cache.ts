import { InMemoryCache } from "@apollo/client";

/**
 * Deliberately untuned: no list type policies, no merge functions. The cache
 * is a transport detail, not the source of truth. See repo-rules.md §7.
 */
export const cache = new InMemoryCache();
