#!/usr/bin/env python3
import argparse, json, subprocess, sys, os
import logging
from datetime import datetime

ESMINI_BIN = os.environ.get("ESMINI_BIN", "/opt/esmini/bin/esmini")

# Create timestamp for this whole regression run
TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
LOGS_DIR = "logs"
MASTER_LOG = f"{LOGS_DIR}/regression_{TIMESTAMP}.log"

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Custom log formatter
class RegressionFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname.upper()
        return f"{timestamp} [REGRESSION][{level}] {record.getMessage()}"

# Configure logger
logger = logging.getLogger("regression")
logger.setLevel(logging.INFO)

formatter = RegressionFormatter()

file_handler = logging.FileHandler(MASTER_LOG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def run_regression(config, run_id=None):
    scenario = config["scenario"]
    duration = config.get("duration", 30)
    expected = config.get("expected_result")
    run_label = f" (run {run_id})" if run_id is not None else ""
    logger.info(f"Running scenario: {scenario} for {duration}s (expect: {expected}){run_label}")

    try:
        result = subprocess.run(
            [ESMINI_BIN, "--osc", f"scenarios/{scenario}", "--headless"],
            capture_output=True, text=True, timeout=duration+10
        )
    except subprocess.TimeoutExpired:
        logger.error(f"Scenario {scenario}{run_label} timed out")
        return False

    base_name = os.path.splitext(scenario)[0]
    log_suffix = f"_run{run_id}" if run_id is not None else ""
    timestamped = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = f"{LOGS_DIR}/{base_name}{log_suffix}_{timestamped}.log"

    with open(log_file, "w") as f:
        f.write(result.stdout)

    # Validation checks
    if expected == "no_collision" and "COLLISION" in result.stdout:
        logger.error(f"Failed: Collision detected in {scenario}{run_label}")
        return False
    elif expected == "safe_distance" and "Unsafe distance" in result.stdout:
        logger.error(f"Failed: Unsafe distance in {scenario}{run_label}")
        return False
    elif expected == "error" and "cannot open" in result.stdout:
        logger.error(f"Failed: {scenario}{run_label} could not open")
        logger.debug(result.stdout)
        return False

    logger.info(f"Passed: {scenario}{run_label}, log saved at {log_file}")
    return True

def summarize_config(configs):
    """Print a summary of all scenarios without running them."""
    logger.info("Dry-run summary:")
    for i, c in enumerate(configs, 1):
        scenario = c.get("scenario", "unknown")
        duration = c.get("duration", 30)
        expected = c.get("expected_result", "not specified")
        runs = c.get("runs", 1)
        logger.info(f" {i}. Scenario: {scenario}, Duration: {duration}s, Expected: {expected}, Runs: {runs}")

def load_config(path):
    """Load config file and normalize into a list of scenarios."""
    with open(path, "r") as f:
        config = json.load(f)
    if isinstance(config, dict):   # single scenario
        return [config]
    elif isinstance(config, list): # multiple scenarios
        return config
    else:
        raise ValueError("Config must be a dict (single scenario) or list (multiple scenarios)")

def main():
    parser = argparse.ArgumentParser(description="ESmini Regression Runner")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    parser.add_argument("--dry-run", action="store_true", help="Only parse and summarize config without running")
    args = parser.parse_args()

    try:
        configs = load_config(args.config)
    except Exception as e:
        logger.error(f"Error reading config: {e}")
        sys.exit(1)

    if args.dry_run:
        summarize_config(configs)
        sys.exit(0)

    logger.info(f"=== Regression started at {TIMESTAMP} ===")

    # Run all scenarios (with multiple runs)
    all_success = True
    for c in configs:
        runs = c.get("runs", 1)
        for run_idx in range(1, runs + 1):
            success = run_regression(c, run_id=run_idx if runs > 1 else None)
            if not success:
                all_success = False

    logger.info(f"=== Regression finished. Result: {'PASS' if all_success else 'FAIL'} ===")
    logger.info(f"Master log written to {MASTER_LOG}")
    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()

