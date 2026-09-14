import { createBrowserRouter } from "react-router";

import SignInController from "../features/auth/controllers/SignInController/SignInController";
import SignUpController from "../features/auth/controllers/SignUpController/SignUpController";
import VerifyEmailController from "../features/auth/controllers/VerifyEmailController/VerifyEmailController";
import CommandCenterController from "../features/capture/controllers/CommandCenterController/CommandCenterController";
import RecordDetailController from "../features/records/controllers/RecordDetailController/RecordDetailController";
import RecordsController from "../features/records/controllers/RecordsController/RecordsController";
import SettingsController from "../features/settings/controllers/SettingsController/SettingsController";
import AppShell from "./AppShell";
import RequireAuth from "./RequireAuth";

export const router = createBrowserRouter([
  { path: "/sign-up", element: <SignUpController /> },
  { path: "/verify-email", element: <VerifyEmailController /> },
  { path: "/sign-in", element: <SignInController /> },
  {
    element: <RequireAuth />,
    children: [
      {
        element: <AppShell />,
        children: [
          { path: "/", element: <CommandCenterController /> },
          { path: "/records", element: <RecordsController /> },
          { path: "/records/:id", element: <RecordDetailController /> },
          { path: "/settings", element: <SettingsController /> },
        ],
      },
    ],
  },
]);
