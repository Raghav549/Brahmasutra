#!/bin/bash

echo "Building APK..."

cd "/data/data/com.termux/files/home/सूत्र-तंत्र/निर्माण/ganga_apk"

gradle assembleDebug

echo "APK build complete"

echo "Install command:"

echo "adb install app/build/outputs/apk/debug/app-debug.apk"
