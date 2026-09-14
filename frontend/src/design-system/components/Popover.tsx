import { cva, type VariantProps } from "class-variance-authority";
import { useEffect, useRef, useState, type ReactElement, type ReactNode } from "react";

import { cn } from "../../utils/cn";

const popoverContentVariants = cva(
  "absolute z-50 min-w-[200px] rounded-md border border-border-strong bg-card py-1.5 shadow-lg",
  {
    variants: {
      placement: {
        "bottom-start": "top-full left-0 mt-1.5",
        "bottom-end": "top-full right-0 mt-1.5",
        "top-start": "bottom-full left-0 mb-1.5",
        "top-end": "bottom-full right-0 mb-1.5",
      },
    },
    defaultVariants: {
      placement: "bottom-start",
    },
  },
);

export interface PopoverTriggerRenderProps {
  isOpen: boolean;
  toggle: () => void;
}

export interface PopoverContentRenderProps {
  close: () => void;
}

export interface PopoverProps extends VariantProps<typeof popoverContentVariants> {
  trigger: (props: PopoverTriggerRenderProps) => ReactElement;
  children: ReactNode | ((props: PopoverContentRenderProps) => ReactNode);
  className?: string;
  // Applied to the positioning wrapper around the trigger (which is what an
  // ancestor flex/grid container actually lays out) rather than to the
  // trigger element itself — needed for anything that must affect the
  // wrapper's own box, e.g. `mt-auto` to pin it within a flex column.
  containerClassName?: string;
}

// A generic trigger+panel primitive: open state, click-outside-to-close,
// Escape-to-close, positioned near its trigger. Knows nothing about what it
// contains — callers supply the trigger element and the panel content.
const Popover = (props: PopoverProps): ReactElement => {
  const { trigger, children, placement, className, containerClassName } = props;
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const close = (): void => setIsOpen(false);
  const toggle = (): void => setIsOpen((previousIsOpen) => !previousIsOpen);

  useEffect(() => {
    if (!isOpen) return;

    const handlePointerDown = (event: PointerEvent): void => {
      const container = containerRef.current;
      if (container && !container.contains(event.target as Node)) {
        close();
      }
    };
    const handleKeyDown = (event: KeyboardEvent): void => {
      if (event.key === "Escape") close();
    };

    document.addEventListener("pointerdown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("pointerdown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  return (
    <div ref={containerRef} className={cn("relative", containerClassName)}>
      {trigger({ isOpen, toggle })}
      {isOpen && (
        <div className={cn(popoverContentVariants({ placement }), className)} role="menu">
          {typeof children === "function" ? children({ close }) : children}
        </div>
      )}
    </div>
  );
};

export default Popover;
