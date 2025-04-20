import os
import shutil


def copy_directory(src_dir, dest_dir):
    # Remove destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        # Calculate the corresponding destination path
        dest_root = os.path.join(dest_dir, os.path.relpath(root, src_dir))

        # Create directories in destination
        for dir_name in dirs:
            dest_path = os.path.join(dest_root, dir_name)
            os.makedirs(dest_path, exist_ok=True)

        # Copy files
        for file_name in files:
            src_path = os.path.join(root, file_name)
            dest_path = os.path.join(dest_root, file_name)
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_path} -> {dest_path}")


def main():
    copy_directory("static", "public")


if __name__ == "__main__":
    main()
