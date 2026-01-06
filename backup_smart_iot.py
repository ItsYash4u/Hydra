import os
import shutil

# Configuration
SOURCE_ROOT = r"C:\Users\AYUSH\OneDrive\Desktop\admin\Greeva"
DEST_ROOT = os.path.join(SOURCE_ROOT, "Smart_IoT_Backup_Final")

FILES_TO_BACKUP = [
    r"greeva\templates\pages\hydroponics-dashboard.html",
    r"greeva\templates\pages\measurement.html",
    r"greeva\templates\pages\services.html",
    r"greeva\templates\partials\sidenav.html",
    r"greeva\templates\base.html",
    r"greeva\pages\views.py",
    r"greeva\pages\urls.py",
    r"greeva\hydroponics\views.py",
    r"greeva\hydroponics\urls.py",
    r"greeva\users\signals.py",
    r"greeva\hydroponics\models.py"
]

def backup_files():
    print(f"Creating backup directory: {DEST_ROOT}")
    if not os.path.exists(DEST_ROOT):
        try:
            os.makedirs(DEST_ROOT)
        except Exception as e:
            print(f"Error creating directory: {e}")
            return

    success_count = 0
    
    for relative_path in FILES_TO_BACKUP:
        src_path = os.path.join(SOURCE_ROOT, relative_path)
        dest_path = os.path.join(DEST_ROOT, relative_path)
        
        # Create subdirectories if needed
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                print(f"Error creating subdir {dest_dir}: {e}")
                continue
        
        if os.path.exists(src_path):
            try:
                shutil.copy2(src_path, dest_path)
                print(f"[OK] Backed up: {relative_path}")
                success_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to backup {relative_path}: {e}")
        else:
            print(f"[MISSING] Source file not found: {relative_path}")

    print(f"\nBackup complete. {success_count}/{len(FILES_TO_BACKUP)} files saved to Smart_IoT_Backup_Final")

if __name__ == "__main__":
    backup_files()
