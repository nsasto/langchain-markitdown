# sync_requirements.py

import importlib.util
import pathlib
import sys

SETUP_PY = "setup.py"
REQUIREMENTS_TXT = "requirements.txt"

def load_setup_module(setup_path):
    spec = importlib.util.spec_from_file_location("setup_module", setup_path)
    setup_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup_module)
    return setup_module

def write_requirements_txt(requirements):
    path = pathlib.Path(REQUIREMENTS_TXT)
    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(requirements) + "\n")

def main():
    try:
        setup_module = load_setup_module(SETUP_PY)
        install_requires = getattr(setup_module, "install_requires", None)

        if not install_requires:
            print("No 'install_requires' found in setup.py.")
            sys.exit(1)

        print(f"Found {len(install_requires)} dependencies. Writing to {REQUIREMENTS_TXT}...")
        write_requirements_txt(install_requires)
        print("Sync complete.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
