import { cva, type VariantProps } from "class-variance-authority";
import type { ButtonHTMLAttributes, ReactElement } from "react";

import { cn } from "../../utils/cn";

const buttonVariants = cva(
  "inline-flex items-center gap-1.5 rounded-md border font-medium font-sans transition-colors disabled:cursor-not-allowed disabled:opacity-60",
  {
    variants: {
      variant: {
        default: "border-border-strong bg-card text-foreground",
        primary: "border-accent bg-accent text-white",
        danger: "border-destructive bg-destructive text-white",
      },
      size: {
        default: "h-10 px-4 text-[13.5px]",
        sm: "h-8 px-2.5 text-[12.5px]",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = (props: ButtonProps): ReactElement => {
  const { className, variant, size, ...rest } = props;
  return <button className={cn(buttonVariants({ variant, size }), className)} {...rest} />;
};

export default Button;
