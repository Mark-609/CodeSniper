#!/usr/bin/env python3
import argparse
import time

def generate_all_combinations(length):
    total = 10 ** length
    for i in range(total):
        yield str(i).zfill(length)

def automate_typing(codes, interval=0.05, delete_after=True,
                    countdown=5, disable_failsafe=False):
    import pyautogui

    if disable_failsafe:
        pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.0

    if countdown > 0:
        print(f"Starting in {countdown} seconds. Focus on the typing box...")
        for i in range(countdown, 0, -1):
            print(i, end=" ", flush=True)
            time.sleep(1)
        print("\nStarting now...\n")

    for idx, code in enumerate(codes, start=1):
        print(f"[{idx}] Typing: {code}")
        pyautogui.write(code)
        pyautogui.press("enter")

        if delete_after:
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(
        description="Generate and type numeric sequences"
    )

    parser.add_argument("--all-combinations",
                        action="store_true",
                        help="Generate all numeric combinations of given length")

    parser.add_argument("--type", action="store_true",
                        help="Enable auto typing")

    parser.add_argument("-l", "--length", type=int, default=1,
                        help="Length of numeric combinations")

    parser.add_argument("--interval", type=float, default=0.05)
    parser.add_argument("--countdown", type=int, default=5)
    parser.add_argument("--no-delete", action="store_true")
    parser.add_argument("--disable-failsafe", action="store_true")
    parser.add_argument("--force", action="store_true")

    args = parser.parse_args()

    if args.all_combinations:
        total = 10 ** args.length
        if total > 1000 and args.type and not args.force:
            raise SystemExit(
                f"Refusing to type {total:,} combinations without --force"
            )
        codes = generate_all_combinations(args.length)
        print(f"Generating ALL combinations of length {args.length}")
        print(f"→ Total: {total:,} combinations\n")
    else:
        raise SystemExit("You must use --all-combinations in this mode.")

    if args.type:
        automate_typing(
            codes,
            interval=args.interval,
            delete_after=not args.no_delete,
            countdown=args.countdown,
            disable_failsafe=args.disable_failsafe
        )

if __name__ == "__main__":
    main()
