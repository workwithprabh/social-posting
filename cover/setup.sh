#!/usr/bin/env bash
# One-time setup inside the working folder (run from the folder that will hold the cover files)
set -e
npm i -s @fontsource/anton@5.3.0 @fontsource/montserrat@5.3.0
pip install --break-system-packages -q rembg==2.0.86 onnxruntime opencv-python-headless pillow numpy
# Playwright + Chromium are assumed pre-installed (require('playwright') must work). Do NOT reinstall.
