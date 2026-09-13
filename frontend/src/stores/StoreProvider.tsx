import { createContext, useContext, useState, type ReactNode, type ReactElement } from "react";

import { RootStore } from "./RootStore";

const StoreContext = createContext<RootStore | null>(null);

interface StoreProviderProps {
  children: ReactNode;
}

export const StoreProvider = (props: StoreProviderProps): ReactElement => {
  const { children } = props;
  const [store] = useState(() => new RootStore());

  return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>;
};

export const useStore = (): RootStore => {
  const store = useContext(StoreContext);
  if (store === null) {
    throw new Error("useStore must be used within a StoreProvider");
  }
  return store;
};
