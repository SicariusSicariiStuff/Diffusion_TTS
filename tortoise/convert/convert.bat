@echo off
rm .\in\.gitkeep
rm .\out\.gitkeep
for %%a in (".\in\*.*") do ffmpeg -i "%%a" -ac 1 ".\out\%%~na.wav"