import { useEffect, useState, type ReactElement } from "react";
import { Navigate, Outlet } from "react-router";

import useGetMe from "../api/queries/GetMe/useGetMe";
import { useResponseHandler } from "../api/queries/GetMe/responseHandler";
import { supabaseClient } from "../api/lib/supabaseClient";
import { useStore } from "../stores/StoreProvider";

type SessionStatusType = "CHECKING" | "AUTHENTICATED" | "UNAUTHENTICATED";

// The route guard named in process-docs/002-authentication's implementation
// plan index, section 4: wraps every route that needs a session. No session:
// redirect to /sign-in. Every route inside this one may assume `store.auth`
// is populated once rendered.
const RequireAuth = (): ReactElement | null => {
  const store = useStore();
  const [sessionStatus, setSessionStatus] = useState<SessionStatusType>("CHECKING");

  const { triggerAPI: triggerGetMe, data } = useGetMe();
  const { handleResponse } = useResponseHandler();

  useEffect(() => {
    let isCancelled = false;

    supabaseClient.auth.getSession().then(({ data: sessionData }) => {
      if (isCancelled) return;
      setSessionStatus(sessionData.session !== null ? "AUTHENTICATED" : "UNAUTHENTICATED");
    });

    const { data: subscription } = supabaseClient.auth.onAuthStateChange((_event, session) => {
      if (session === null) {
        store.auth.clear();
        setSessionStatus("UNAUTHENTICATED");
        return;
      }
      setSessionStatus("AUTHENTICATED");
    });

    return () => {
      isCancelled = true;
      subscription.subscription.unsubscribe();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (sessionStatus !== "AUTHENTICATED") return;
    triggerGetMe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionStatus]);

  useEffect(() => {
    if (!data) return;
    handleResponse({
      data,
      onMeLoaded: (me) => store.auth.setMe(me),
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  if (sessionStatus === "CHECKING") return null;
  if (sessionStatus === "UNAUTHENTICATED") return <Navigate to="/sign-in" replace />;

  return <Outlet />;
};

export default RequireAuth;
