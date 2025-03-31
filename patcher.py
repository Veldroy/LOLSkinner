import os
import shutil

class SkinPatcher:
    def __init__(self):
        self.backup_suffix = "_backup"

    def backup_original_files(self, champion, lol_path):
        champ_dir = os.path.join(lol_path, "Game", "DATA", "Characters", champion)
        backup_dir = champ_dir + self.backup_suffix
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            for file in os.listdir(champ_dir):
                if file.endswith((".skn", ".skl", ".dds", ".anm")):
                    src = os.path.join(champ_dir, file)
                    dst = os.path.join(backup_dir, file)
                    shutil.copy(src, dst)
            print(f"Backup created for champion {champion} at {backup_dir}")
        else:
            print(f"Backup already exists for champion {champion}")

    def inject_skin_files(self, champion, skin_path, lol_path):
        champ_dir = os.path.join(lol_path, "Game", "DATA", "Characters", champion)
        # Copy skin files from the custom skin folder to the champion directory.
        for file in os.listdir(skin_path):
            src = os.path.join(skin_path, file)
            dst = os.path.join(champ_dir, file)
            shutil.copy(src, dst)
        print(f"Injected skin files for champion {champion} from {skin_path}")

    def restore_original_files(self, champion, lol_path):
        champ_dir = os.path.join(lol_path, "Game", "DATA", "Characters", champion)
        backup_dir = champ_dir + self.backup_suffix
        if os.path.exists(backup_dir):
            for file in os.listdir(backup_dir):
                src = os.path.join(backup_dir, file)
                dst = os.path.join(champ_dir, file)
                shutil.copy(src, dst)
            print(f"Restored original files for champion {champion}")
        else:
            print(f"No backup found for champion {champion}")
