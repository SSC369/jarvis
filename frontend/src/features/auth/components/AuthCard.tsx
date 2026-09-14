import type { ReactElement, ReactNode } from "react";

import * as Styles from "./styles";

interface AuthCardProps {
  children: ReactNode;
  footer?: ReactNode;
}

const AuthCard = (props: AuthCardProps): ReactElement => {
  const { children, footer } = props;

  return (
    <div className={Styles.pageStyles}>
      <div className={Styles.vignetteStyles} />
      <div className={Styles.wrapStyles}>
        <div className={Styles.colStyles}>
          <div className={Styles.wordmarkStyles}>
            <div className={Styles.markStyles}>
              <svg viewBox="0 0 48 48" width="21" height="21">
                <path d="M31.5 6 L40 6 L18.5 42 L10 42 Z" fill="currentColor" />
              </svg>
            </div>
            <span className={Styles.wtextStyles}>
              slash<span className={Styles.wtextDotStyles}>.</span>it
            </span>
          </div>
          <div className={Styles.cardStyles}>{children}</div>
          {footer !== undefined ? <div className={Styles.footerStyles}>{footer}</div> : null}
        </div>
      </div>
    </div>
  );
};

export default AuthCard;
