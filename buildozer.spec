[app]

# (str) Title of your application
title = Translator

# (str) Package name
package.name = translator

# (str) Package domain (needed for android/iOS packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,png

# (list) Source files to exclude (let empty to not exclude any files)
# source.exclude_exts = spec

# (list) Lists to exclude (let empty to not exclude any files)
# source.exclude_dirs = tests, bin

# (str) Version of your application,想像 for version control
version = 1.0.0

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Required packages/pypi entries
requirements = python3,kivy,requests,certifi

# (list) Application audience
# audience =

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25c

# (str) Android NDK API to use
android.ndk_api = 21

# (bool) Use private site-packages or venv
# p4a.private_site_packages = False

# (bool) VENV folder to prevent initial pip download overhead
# p4a.venv = False

# (str) The Android bootstrap to use
p4a.bootstrap = sdl2

# (list) Android architecture targets
p4a.archs = armeabi-v7a, arm64-v8a

# (bool) Keep your app .PY pure (no compiled .so)
# p4a.preserve_python_main = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin
