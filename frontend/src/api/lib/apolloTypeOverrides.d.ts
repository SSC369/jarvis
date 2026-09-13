import "@apollo/client";

// Declaring a non-optional errorPolicy here is required by Apollo Client
// 4.2 before defaultOptions.errorPolicy: "all" (apolloClient.ts) type-checks
// at all, but it also switches every hook to "modern" signatures, which
// reject the manually specified <Data, Variables> generics our hand-written
// hooks pass to useMutation. @graphql-codegen/typescript-react-apollo (v5)
// predates modern signatures and does not emit TypedDocumentNode, which is
// what modern signatures need to infer those types instead. Pinning
// signatureStyle back to "classic" keeps the generated types working; the
// Apollo changelog names this exact combination for migration.
declare module "@apollo/client" {
  namespace ApolloClient {
    namespace DeclareDefaultOptions {
      interface WatchQuery {
        errorPolicy: "all";
      }
      interface Query {
        errorPolicy: "all";
      }
      interface Mutate {
        errorPolicy: "all";
      }
    }
  }

  export interface TypeOverrides {
    signatureStyle: "classic";
  }
}
