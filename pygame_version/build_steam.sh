#!/bin/bash
# Steam Build Script für Agent Battle Simulator
# Erstellt Executable für Windows, macOS und Linux

set -e

echo "🎮 Agent Battle Simulator - Steam Build"
echo "========================================"

# Check PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installiere PyInstaller..."
    pip3 install pyinstaller
fi

# Build Directory
BUILD_DIR="build/steam"
mkdir -p "$BUILD_DIR"

echo ""
echo "🔨 Building Executable..."

# PyInstaller Build
pyinstaller \
    --name="AgentBattleSimulator" \
    --onefile \
    --windowed \
    --icon=assets/icon.ico \
    --add-data="assets:assets" \
    --add-data="src:src" \
    --hidden-import=pygame \
    --hidden-import=src.pygame_ui \
    --hidden-import=src.multiplayer \
    --hidden-import=src.skins \
    battle_sim_pygame.py

echo ""
echo "✅ Build abgeschlossen!"
echo "📦 Executable: dist/AgentBattleSimulator"

# Steam-Struktur erstellen
echo ""
echo "📁 Erstelle Steam-Struktur..."

STEAM_DIR="$BUILD_DIR/steam_build"
mkdir -p "$STEAM_DIR"

# Copy Executable
cp -r dist/AgentBattleSimulator "$STEAM_DIR/"

# Copy Steam-Config
cp steam/steam_config.json "$STEAM_DIR/"
cp steam/achievements.json "$STEAM_DIR/"

# Copy README
cp README_PYGAME.md "$STEAM_DIR/README.txt"

echo ""
echo "✅ Steam-Build fertig!"
echo "📂 Location: $STEAM_DIR"
echo ""
echo "🚀 Nächste Schritte:"
echo "   1. Teste das Executable: $STEAM_DIR/AgentBattleSimulator"
echo "   2. Upload zu Steam via Steamworks"
echo "   3. Siehe steam/STEAM_RELEASE_GUIDE.md für Details"
