import { createBrowserRouter } from "react-router";

import CommandCenterController from "../features/capture/controllers/CommandCenterController/CommandCenterController";
import RecordDetailController from "../features/records/controllers/RecordDetailController/RecordDetailController";
import RecordsController from "../features/records/controllers/RecordsController/RecordsController";
import SettingsController from "../features/settings/controllers/SettingsController/SettingsController";
import AppShell from "./AppShell";

export const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { path: "/", element: <CommandCenterController /> },
      { path: "/records", element: <RecordsController /> },
      { path: "/records/:id", element: <RecordDetailController /> },
      { path: "/settings", element: <SettingsController /> },
    ],
  },
]);
