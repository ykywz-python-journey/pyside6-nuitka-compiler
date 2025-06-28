# pyside6 nutika compiler
ini adalah contoh aplikasi pyside6 yang dicompile menggunakan nuitka

# requirements
- python 3.12
- uv package manager

## how to use
- run command uv:
  - uv sync
  - uv run build/nuitka_cmd.py

## Command list
```commandline
--standalone
--follow-imports
--enable-plugin=pyside6
--include-data-dir=thirdparty=thirdparty
--windows-icon-from-ico=app.ico
--include-data-files=app.ico=app.ico
--windows-console-mode=disable / --console=force
--output-filename="Pyside6 Nuitka"
--output-dir="C:/output/"
```

## One File
```commandline
--onefile
--onefile-cache-mode=cached
--onefile-tempdir-spec="{CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}"
```

```commandline
{CACHE_DIR} = C:\Users\SomeBody\AppData\Local
{COMPANY} = --company-name
{PRODUCT} = --product-name
```

## Trademark 
```commandline
--company-name=Ykywz
--product-name="Pyside6 Nuitka"
--file-version=1.0.0.0
--product-version=1.0.0.0
--file-description="Compile python use nuitka"
--copyright=irfanykywz
--trademarks=yotrademark
```

## Playground

onedir

```commandline
nuitka --mingw64 --enable-plugin=pyside6 --windows-icon-from-ico=app.png --include-data-dir=thirdparty=thirdparty --include-data-files=app.png=app.png --windows-console-mode=disable --standalone main.py
```

onefile

```commandline
nuitka --mingw64 --enable-plugin=pyside6 --windows-icon-from-ico=app.png --include-data-dir=thirdparty=thirdparty --include-data-files=app.png=app.png --windows-console-mode=disable --standalone main.py
```

onefile full version + static cached

```commandline
nuitka --mingw64 --enable-plugin=pyside6 --windows-icon-from-ico=app.png --include-data-dir=thirdparty=thirdparty --include-data-files=app.png=app.png --windows-console-mode=disable --standalone --company-name=Ykywz --product-name="Pyside6 Nuitka Ykywz" --file-version=1.2 --product-version=1.2 --file-description="Ykywz Compile python use nuitka" --copyright=irfanykywz --trademarks=yotrademark --onefile --onefile-cache-mode=cached --onefile-tempdir-spec="{CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}" --output-filename="Pyside6 Nuitka" --output-dir="C:/output/" main.py
```