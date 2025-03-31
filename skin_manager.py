import os
import json
from patcher import SkinPatcher

class SkinManager:
    def __init__(self):
        self.skins_repo = self.load_skins_repository()
        self.patcher = SkinPatcher()

    def load_skins_repository(self):
        """
        Loads skin data from a JSON file.
        Expected JSON structure:
        {
            "skins": [
                { "name": "Custom Ashe", "path": "./skins/ashe_custom" },
                { "name": "Custom Garen", "path": "./skins/garen_custom" }
            ]
        }
        """
        try:
            with open("skins_repository.json", "r") as f:
                data = json.load(f)
            return data.get("skins", [])
        except Exception as e:
            print(f"Error loading skins repository: {e}")
            return []

    def get_available_skins(self):
        return [skin["name"] for skin in self.skins_repo]

    def get_skin_path(self, skin_name):
        for skin in self.skins_repo:
            if skin["name"] == skin_name:
                return skin["path"]
        return None

    def apply_skin(self, skin_name, skin_path, lol_path):
        try:
            # Assume champion folder is deduced from the skin_path folder name.
            champion = os.path.basename(skin_path).split("_")[0]
            self.patcher.backup_original_files(champion, lol_path)
            self.patcher.inject_skin_files(champion, skin_path, lol_path)
            return True
        except Exception as e:
            print(f"Error applying skin {skin_name}: {e}")
            return False

    def restore_skin(self, lol_path):
        try:
            # For simplicity, iterate through the repository to restore backups.
            for skin in self.skins_repo:
                champion = os.path.basename(skin["path"]).split("_")[0]
                self.patcher.restore_original_files(champion, lol_path)
            return True
        except Exception as e:
            print(f"Error restoring skins: {e}")
            return False
