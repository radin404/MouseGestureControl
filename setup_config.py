import json
import os

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "up": "task_view",
    "down": "close_task_view",
    "left": "desktop_right",
    "right": "desktop_left",
    "debug": True,
    "threshold": 80,
    "cooldown": 0.5,
    "use_alt_instead_of_ctrl": False
}


def load_config():
    """Load config or create one if missing."""
    if not os.path.exists(CONFIG_PATH):
        print("⚠️ No config.json found. Creating a new one with defaults.")
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(cfg):
    """Save config to file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)
    print("\n✅ Config saved successfully!")


def show_config(cfg):
    print("\n🧭 Current Configuration:")
    print("-" * 40)
    for k, v in cfg.items():
        print(f"{k:<25}: {v}")
    print("-" * 40)


def toggle_bool(cfg, key):
    cfg[key] = not cfg[key]
    print(f"🔁 {key} set to {cfg[key]}")


def set_numeric(cfg, key, value_type=float):
    try:
        val = value_type(input(f"Enter new {key} value: ").strip())
        cfg[key] = val
        print(f"✅ {key} updated to {val}")
    except ValueError:
        print("⚠️ Invalid number, keeping previous value.")


def menu():
    cfg = load_config()

    while True:
        show_config(cfg)
        print("""
🛠  Configuration Menu
1. Toggle Debug Mode
2. Set Threshold (gesture distance)
3. Set Cooldown (seconds)
4. Toggle Alt instead of Ctrl
5. Restore Defaults
6. Save & Exit
7. Exit Without Saving
""")
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            toggle_bool(cfg, "debug")
        elif choice == "2":
            set_numeric(cfg, "threshold", float)
        elif choice == "3":
            set_numeric(cfg, "cooldown", float)
        elif choice == "4":
            toggle_bool(cfg, "use_alt_instead_of_ctrl")
        elif choice == "5":
            confirm = input("Reset all settings to default? (y/n): ").lower()
            if confirm == "y":
                cfg = DEFAULT_CONFIG.copy()
                print("🔄 Restored default configuration.")
        elif choice == "6":
            save_config(cfg)
            break
        elif choice == "7":
            print("❌ Exiting without saving changes.")
            break
        else:
            print("⚠️ Invalid choice. Try again.")


if __name__ == "__main__":
    print("🧩 MouseGestureControl Configurator")
    menu()
