import os
import datetime
import shutil

BRAIN_PATH = ".gemini/brain"
EPISODES_PATH = os.path.join(BRAIN_PATH, "episodes")
DEVLOG_PATH = "docs/DEVLOG.md"

def sync_memory():
    """Syncs the current session content to episodic memory."""
    today = datetime.date.today().isoformat()
    episode_file = os.path.join(EPISODES_PATH, f"session_{today}.md")

    if not os.path.exists(DEVLOG_PATH):
        print(f"⚠️ No DEVLOG found at {DEVLOG_PATH}")
        return

    print(f"🧠 Syncing memory to {episode_file} ...")
    
    # Simple Append Strategy for MVP
    # In future: Parse specific sections
    try:
        shutil.copy2(DEVLOG_PATH, episode_file)
        print("✅ Episodic memory consolidated.")
    except Exception as e:
        print(f"❌ Failed to sync memory: {e}")

if __name__ == "__main__":
    sync_memory()
