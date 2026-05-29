[app]
title = Nation Wants to Guess
package.name = nationwantstoguess
package.domain = org.nwtg

source.dir = ./frontend
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png

permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.gradle_dependencies = 

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.features = android.hardware.touchscreen

requirements = python3,kivy,kivymd,requests,sqlalchemy,fastapi,uvicorn

android.bootstrap = sdl2
android.archs = arm64-v8a,armeabi-v7a

android.release_artifact = apk

android.logcat_filters = *:S python:D

# Build configuration
p4a.url = https://github.com/kivy/python-for-android/archive/master.zip
p4a.private_storage_dir = .buildozer/android/platform/build-<app.package.name>-<android.release_artifact>

android.gradle_options = org.gradle.jvmargs=-Xmx4096m

android.minapi = 21
android.targetapi = 33
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
