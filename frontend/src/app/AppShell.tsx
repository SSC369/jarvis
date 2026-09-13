import { Command, List, Settings } from "lucide-react";
import type { ReactElement } from "react";
import { NavLink, Outlet } from "react-router";

import { cn } from "../utils/cn";
import * as Styles from "./styles";

interface NavItemProps {
  to: string;
  label: string;
  icon: ReactElement;
}

const NAV_ITEMS: NavItemProps[] = [
  { to: "/", label: "Capture", icon: <Command size={20} /> },
  { to: "/records", label: "Records", icon: <List size={20} /> },
  { to: "/settings", label: "Settings", icon: <Settings size={20} /> },
];

const AppShell = (): ReactElement => {
  return (
    <div className={Styles.shellStyles}>
      <div className={Styles.railStyles}>
        <div className={Styles.brandRowStyles}>
          <div className={Styles.brandMarkStyles}>
            <svg viewBox="0 0 48 48" width="15" height="15">
              <path d="M31.5 6 L40 6 L18.5 42 L10 42 Z" fill="currentColor" />
            </svg>
          </div>
          <span className={Styles.wordmarkStyles}>
            slash<span className={Styles.wordmarkDotStyles}>.</span>it
          </span>
        </div>
        <nav className={Styles.navStyles}>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                cn(Styles.navItemStyles, isActive && Styles.navItemOnStyles)
              }
            >
              {item.icon}
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className={Styles.railFootStyles}>
          <div className={Styles.avatarStyles}>Y</div>
          <div className="min-w-0">
            <div className={Styles.accountNameStyles}>Your account</div>
            <div className={Styles.accountEmailStyles}>you@example.com</div>
          </div>
        </div>
      </div>
      <div className={Styles.mainStyles}>
        <Outlet />
      </div>
    </div>
  );
};

export default AppShell;
