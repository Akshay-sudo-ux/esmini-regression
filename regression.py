#!/usr/bin/env python3
import argparse, json, subprocess, sys, os

ESMINI_BIN = os.environ.get("ESMINI_BIN", "/opt/esmini/bin/esmini")

def run_regression(config):
    scenario = config["scenario"]
    duration = config.get("duration", 30)
    expected = config.get("expected_result")
    print(f"▶ Running scenario: {scenario} for {duration}s (expect: {expected})")

    try:
        result = subprocess.run(
            [ESMINI_BIN, "--osc", f"scenarios/{scenario}", "--headless"],
            capture_output=True, text=True, timeout=duration+10
        )
    except subprocess.TimeoutExpired:
        print(f"Scenario {scenario} timed out")
        return False

    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/{os.path.splitext(scenario)[0]}.log"
    with open(log_file, "w") as f:
        f.write(result.stdout)

    if expected == "no_collision" and "COLLISION" in result.stdout:
        print(f"Failed: Collision detected")
        return False
    elif expected == "safe_distance" and "Unsafe distance" in result.stdout:
        print(f"Failed: Unsafe distance")
        return False
    elif expected == "error" and "cannot open" in result.stdout:
        print(f"Failed: {scenario}")
        print(result.stdout)
        return False
    print(result.stdout)
    print(f"Log file can be found at {log_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description="ESmini Regression Runner")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    args = parser.parse_args()

    try:
        with open(args.config, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)

    success = run_regression(config)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

