import subprocess
import sys
from pathlib import Path


def compile_with_nuitka(
        input_file,
        output_dir,
        project_name,
        project_desc,
        version,
        icon_file,
        data_files,
        data_dirs,
        plugins,
        company_name,
        console_mode,
        onefile
):

    # Build base command
    command = [
        sys.executable,
        "-m", "nuitka",
        "--mingw64",
        "--standalone",
        "--company-name=" + f"{company_name}",
        "--product-name=" + f"{project_name}",
        "--file-version=" + version,
        "--product-version=" + version,
        "--file-description=" + f"{project_desc}",
        "--copyright=" + company_name,
        "--trademarks=" + company_name,
        "--output-dir=" + output_dir,
        "--output-filename=" + project_name
    ]

    # Add plugins
    for plugin in plugins:
        command.append("--enable-plugin=" + plugin)

    # Add console mode
    if not console_mode:
        command.append("--windows-console-mode=" + "disable")

    # Add onefile options
    if onefile:
        command.extend([
            "--onefile",
            "--onefile-cache-mode=" + "cached",
            "--onefile-tempdir-spec=" + "{CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}"
        ])

    # Add icon if specified
    if icon_file and Path(icon_file).exists():
        command.extend([
            "--windows-icon-from-ico=" + icon_file,
        ])

    # Add data files (multiple --include-data-files)
    if data_files:
        for item in data_files:
            # print(item.get('dest'))
            source = item.get('source')
            dest = item.get('dest')
            if Path(source).exists():
                # print(["--include-data-files=" + f"{source}={dest}"])
                command.extend([f"--include-data-files={source}={dest}"])
            else:
                print(f"Warning: Data file not found: {source}")

    # Add data directories (multiple --include-data-dir)
    if data_dirs:
        for item in data_dirs:
            source = item.get('source')
            dest = item.get('dest')
            if Path(source).exists() and Path(source).is_dir():
                command.extend([f"--include-data-dir={source}={dest}"])
            else:
                print(f"Warning: Data directory not found: {source}")

    command.extend([input_file])

    print("Executing compilation command:")
    print(command)
    # print(" ".join(command))
    # exit()

    try:
        # Execute the Nuitka command using subprocess.Popen()
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            print(line, end='')

        return_code = process.wait()
        if return_code == 0:
            print("Nuitka compilation successful!")
        else:
            print(f"Nuitka compilation failed with return code: {return_code}")

    except FileNotFoundError:
        print("Error: Python executable or Nuitka module not found.")
        print("Ensure Python is in your PATH and Nuitka is installed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Example usage with multiple files and directories
    compile_with_nuitka(
        input_file="../src/main.py",
        output_dir="C:/output/",
        project_name="Pyside6 Nuitka Compile",
        project_desc="Try compile pyside6 with nuitka",
        version="1.3.0.0",
        icon_file="../src/app.png",
        data_files=[
            {"source": "../src/app.png", "dest": "app.png"},
        ],
        data_dirs=[
            {"source": "../src/thirdparty/", "dest": "thirdparty"},
        ],
        plugins=["pyside6"],
        company_name="Ykywz",
        console_mode=False,
        onefile=True
    )
