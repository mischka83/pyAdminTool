#!/usr/bin/env bash
set -e

echo "🧹 Entferne alte Builds..."
rm -rf build dist

echo "📦 Erstelle neuen Build..."
pyinstaller pyadmintool.spec

echo ""
echo "✅ Build erfolgreich!"
echo "👉 Output: dist/pyadmintool"
