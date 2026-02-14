import os
import json
import random
import subprocess
import logging
from datetime import datetime
import time

METRICS_FILE = "metrics.json"
README_FILE = "README.md"
SLEEP_SECONDS = 60  # intervalo pequeno só para visualização


# ---------------------------
# Logging Setup
# ---------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ---------------------------
# Metrics Management
# ---------------------------

def load_metrics():
    if not os.path.exists(METRICS_FILE):
        logger.info("Metrics file not found. Creating new one.")
        return {
            "total_commits": 0,
            "last_commit_at": None,
            "last_push_at": None
        }
    with open(METRICS_FILE, "r") as f:
        return json.load(f)


def save_metrics(metrics):
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.info("Metrics updated successfully.")


# ---------------------------
# Git Operations
# ---------------------------

def git_commit(message):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        logger.info(f"Commit successful: {message}")
    except subprocess.CalledProcessError:
        logger.error("Git commit failed.", exc_info=True)
        raise


def git_push():
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True)
        logger.info("Push successful.")
    except subprocess.CalledProcessError:
        logger.error("Git push failed.", exc_info=True)
        raise


# ---------------------------
# Dice
# ---------------------------

def roll_dice():
    result = random.randint(1, 4)
    logger.info(f"Dice rolled: {result}")
    return result


# ---------------------------
# Main Logic
# ---------------------------

def main():
    logger.info("Starting simple commit tracker.")

    metrics = load_metrics()
    commits_to_make = roll_dice()

    for i in range(commits_to_make):
        logger.info(f"Starting commit {i+1} of {commits_to_make}")

        # Append something to README
        timestamp = datetime.now().isoformat()
        with open(README_FILE, "a", encoding="utf-8") as f:
            f.write(f"\nCommit generated at {timestamp}")

        commit_message = f"Automated commit at {timestamp}"
        git_commit(commit_message)

        # Update metrics
        metrics["total_commits"] += 1
        metrics["last_commit_at"] = timestamp
        save_metrics(metrics)

        time.sleep(SLEEP_SECONDS+commits_to_make)

    logger.info("All commits completed. Starting push.")

    git_push()

    metrics["last_push_at"] = datetime.now().isoformat()
    save_metrics(metrics)

    logger.info("Process finished successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.critical("Fatal error occurred.", exc_info=True)