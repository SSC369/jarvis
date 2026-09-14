import type { AuthError } from "@supabase/supabase-js";
import { Check, CircleAlert } from "lucide-react";
import {
  useEffect,
  useState,
  type ChangeEvent,
  type FormEvent,
  type ReactElement,
} from "react";
import { Link, useNavigate } from "react-router";

import { supabaseClient } from "../../../../api/lib/supabaseClient";
import Button from "../../../../design-system/components/Button";
import { cn } from "../../../../utils/cn";
import AuthCard from "../../components/AuthCard";
import * as Styles from "./styles";

// FR-3: 3-20 characters, letters, numbers and underscores only. Uniqueness
// itself (case-insensitive) is enforced server-side by the `profiles`
// table's expression index; this is format validation only.
const USERNAME_PATTERN = /^[A-Za-z0-9_]{3,20}$/;

const NAVIGATE_TO_VERIFY_DELAY_MS = 750;

type PhaseType = "FORM" | "LIMITED" | "SUCCESS";

type SignUpErrorKindType = "EMAIL_TAKEN" | "USERNAME_TAKEN" | "GENERIC";

interface FieldErrors {
  username?: string;
  email?: string;
  password?: string;
}

// GENERIC_ERROR_MESSAGE: 02-design.md's copy table (§8) covers the taken-email,
// taken-username and rate-limited states, but not a bare network failure or an
// unrecognised signUp error. 04.1's error-handling table (§6) only says such a
// failure gets "a generic retry-safe error, not one of the specific states
// above", without giving exact wording.
// > Assumption: using a short generic retry message here since none is
// > specified; flag for the design owner if different copy is wanted.
const GENERIC_ERROR_MESSAGE = "Something went wrong. Try again.";

const validateFields = (username: string, password: string): FieldErrors => {
  const errors: FieldErrors = {};
  if (!USERNAME_PATTERN.test(username)) {
    errors.username = "3-20 characters: letters, numbers and underscores only.";
  }
  if (password.length === 0) {
    errors.password = "Enter a password.";
  }
  return errors;
};

// Classifies a signUp() error against 04.1-manual-signup-and-signin.md §6's
// error table. Verified live 2026-09-15 against the real Supabase project
// (see 05-dev-log.md's deviation follow-up for T-1.8). EMAIL_TAKEN and
// USERNAME_TAKEN remain unverified — see their comments below.
const RATE_LIMIT_ERROR_CODES = new Set(["over_email_send_rate_limit", "over_request_rate_limit"]);

const classifySignUpError = (error: AuthError): "RATE_LIMITED" | SignUpErrorKindType => {
  const message = error.message.toLowerCase();

  // CONFIRMED LIVE: Supabase's own built-in email-send throttle rejects
  // repeated signups with error_code "over_email_send_rate_limit" (auth-js's
  // ErrorCode union also lists "over_request_rate_limit" for a general
  // per-project throttle). Observed both a 429 AND a plain 400 for this same
  // error_code against the real project, so the HTTP status alone is not a
  // reliable signal — matched primarily on error.code now, with status 429
  // and hook_before_user_created's literal message kept as fallbacks (the
  // hook itself is still unregistered, T-1.4, so that string remains
  // unverified).
  const isKnownRateLimitCode = error.code !== undefined && RATE_LIMIT_ERROR_CODES.has(error.code);
  if (isKnownRateLimitCode || error.status === 429 || message.includes("too many attempts")) {
    return "RATE_LIMITED";
  }

  // Supabase's documented code for signUp on an already-registered,
  // confirmed email.
  if (error.code === "user_already_exists" || message.includes("already registered")) {
    return "EMAIL_TAKEN";
  }

  // GUESS, unverified live (logged in 05-dev-log.md as a deviation): a
  // failed handle_new_user() trigger (0007_profiles.py's unique-username
  // index) aborts the auth.users insert, and GoTrue's documented behaviour
  // for a failed post-insert trigger is a generic 500 with this message.
  // Nothing in this repo has exercised that path against a real project.
  if (message.includes("database error saving new user")) {
    return "USERNAME_TAKEN";
  }

  return "GENERIC";
};

const SignUpController = (): ReactElement => {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [errorKind, setErrorKind] = useState<SignUpErrorKindType | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [phase, setPhase] = useState<PhaseType>("FORM");

  useEffect(() => {
    if (phase !== "SUCCESS") return undefined;
    const timeoutId = window.setTimeout(() => {
      navigate(`/verify-email?email=${encodeURIComponent(email)}`);
    }, NAVIGATE_TO_VERIFY_DELAY_MS);
    return () => window.clearTimeout(timeoutId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase, email]);

  const handleUsernameChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setUsername(event.target.value);
    setFieldErrors((previous) => ({ ...previous, username: undefined }));
    setErrorKind(null);
  };

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setEmail(event.target.value);
    setFieldErrors((previous) => ({ ...previous, email: undefined }));
    setErrorKind(null);
  };

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setPassword(event.target.value);
    setFieldErrors((previous) => ({ ...previous, password: undefined }));
  };

  const handleGoogleSignIn = async (): Promise<void> => {
    await supabaseClient.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: window.location.origin + "/",
        // Google silently re-authenticates on an existing browser session
        // with prior consent, skipping the account chooser. Forcing it
        // keeps "Continue with Google" honest about which account is used.
        queryParams: { prompt: "select_account" },
      },
    });
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();

    const clientErrors = validateFields(username, password);
    const hasClientErrors = clientErrors.username !== undefined || clientErrors.password !== undefined;
    if (hasClientErrors) {
      setFieldErrors(clientErrors);
      return;
    }

    setFieldErrors({});
    setErrorKind(null);
    setIsSubmitting(true);

    try {
      const { error } = await supabaseClient.auth.signUp({
        email,
        password,
        options: { data: { username } },
      });

      if (error) {
        const kind = classifySignUpError(error);
        if (kind === "RATE_LIMITED") {
          setPhase("LIMITED");
          return;
        }
        if (kind === "EMAIL_TAKEN") {
          setErrorKind("EMAIL_TAKEN");
          setFieldErrors((previous) => ({ ...previous, email: "This email is taken" }));
          return;
        }
        if (kind === "USERNAME_TAKEN") {
          setErrorKind("USERNAME_TAKEN");
          setFieldErrors((previous) => ({ ...previous, username: "This username is taken." }));
          return;
        }
        setErrorKind("GENERIC");
        return;
      }

      setPhase("SUCCESS");
    } catch {
      // Network failure, per 04.1 §6: a generic retry-safe error, no
      // optimistic state change.
      setErrorKind("GENERIC");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (phase === "SUCCESS") {
    return (
      <AuthCard>
        <div className={Styles.centerCardStyles}>
          <div className={Styles.successIconWrapStyles}>
            <Check size={24} />
          </div>
          <div className={Styles.statusTitleStyles}>Account created</div>
          <div className={Styles.statusBodyStyles}>Taking you to verify your email next.</div>
        </div>
      </AuthCard>
    );
  }

  if (phase === "LIMITED") {
    return (
      <AuthCard>
        <div className={Styles.centerCardStyles} role="status">
          <div className={Styles.limitedIconWrapStyles}>
            <CircleAlert size={24} />
          </div>
          <div className={Styles.statusTitleStyles}>Too many attempts</div>
          <div className={Styles.statusBodyStyles}>
            Too many accounts have been created from this address recently. Try again in a few
            minutes.
          </div>
        </div>
      </AuthCard>
    );
  }

  return (
    <AuthCard
      footer={
        <>
          Already have an account?{" "}
          <Link to="/sign-in" className={Styles.inlineLinkStyles}>
            Sign in
          </Link>
        </>
      }
    >
      <div className={Styles.titleStyles}>Create your account</div>
      <div className={Styles.subtitleStyles}>One account. Everything you capture, in one place.</div>

      {errorKind !== null ? (
        <div className={Styles.noteErrorStyles} role="alert">
          <CircleAlert size={16} className={Styles.noteErrorIconStyles} />
          <div>
            {errorKind === "EMAIL_TAKEN" ? (
              <>
                That email is already registered.{" "}
                <Link to="/sign-in" className={Styles.inlineLinkStyles}>
                  Sign in instead
                </Link>
                .
              </>
            ) : null}
            {errorKind === "USERNAME_TAKEN" ? "That username is taken." : null}
            {errorKind === "GENERIC" ? GENERIC_ERROR_MESSAGE : null}
          </div>
        </div>
      ) : null}

      <button type="button" className={Styles.googleButtonStyles} onClick={handleGoogleSignIn}>
        <svg width="18" height="18" viewBox="0 0 18 18">
          <path
            fill="#4285F4"
            d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"
          />
          <path
            fill="#34A853"
            d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"
          />
          <path
            fill="#FBBC05"
            d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"
          />
          <path
            fill="#EA4335"
            d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"
          />
        </svg>
        <span>Continue with Google</span>
      </button>
      <div className={Styles.dividerStyles}>
        <span className={Styles.dividerLineStyles} />
        <span>or</span>
        <span className={Styles.dividerLineStyles} />
      </div>

      <form onSubmit={handleSubmit} noValidate>
        <div className={Styles.formRowStyles}>
          <label className={Styles.fieldLabelStyles} htmlFor="signup-username">
            Username
          </label>
          <input
            id="signup-username"
            name="username"
            type="text"
            autoComplete="username"
            placeholder="jordan_p"
            value={username}
            disabled={isSubmitting}
            onChange={handleUsernameChange}
            className={cn(Styles.controlStyles, fieldErrors.username && Styles.controlErrorStyles)}
          />
          {fieldErrors.username ? (
            <div className={Styles.fieldErrorStyles}>{fieldErrors.username}</div>
          ) : null}
        </div>

        <div className={Styles.formRowStyles}>
          <label className={Styles.fieldLabelStyles} htmlFor="signup-email">
            Email
          </label>
          <input
            id="signup-email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="jordan@example.com"
            value={email}
            disabled={isSubmitting}
            onChange={handleEmailChange}
            className={cn(Styles.controlStyles, fieldErrors.email && Styles.controlErrorStyles)}
          />
          {fieldErrors.email ? <div className={Styles.fieldErrorStyles}>{fieldErrors.email}</div> : null}
        </div>

        <div className={Styles.lastFormRowStyles}>
          <label className={Styles.fieldLabelStyles} htmlFor="signup-password">
            Password
          </label>
          <input
            id="signup-password"
            name="password"
            type="password"
            autoComplete="new-password"
            placeholder="••••••••••"
            value={password}
            disabled={isSubmitting}
            onChange={handlePasswordChange}
            className={cn(Styles.controlStyles, fieldErrors.password && Styles.controlErrorStyles)}
          />
          {fieldErrors.password ? (
            <div className={Styles.fieldErrorStyles}>{fieldErrors.password}</div>
          ) : null}
        </div>

        <Button
          type="submit"
          variant="primary"
          disabled={isSubmitting}
          className={Styles.submitButtonStyles}
        >
          {isSubmitting ? (
            <>
              <span className={Styles.spinnerStyles} />
              <span>Creating account&hellip;</span>
            </>
          ) : (
            "Create account"
          )}
        </Button>
      </form>
    </AuthCard>
  );
};

export default SignUpController;
