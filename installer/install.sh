#!/data/data/com.termux/files/usr/bin/bash

echo "====================================="
echo "सूत्र-तंत्र संस्थापन प्रारंभ"
echo "====================================="

INSTALL_DIR="$HOME/सूत्र-तंत्र"

if [ -d "$INSTALL_DIR" ]; then
    echo "सूत्र-तंत्र पहले से उपस्थित है:"
else
    mkdir -p "$INSTALL_DIR"
    echo "निर्देशिका निर्मिता:"
fi

mkdir -p "$INSTALL_DIR/bin"

cp -r "$HOME/सूत्र-तंत्र/release/bin/"* "$INSTALL_DIR/bin/"

chmod +x "$INSTALL_DIR/bin/"*

echo ""
echo "संस्थापन सफल"
echo ""
echo "उपलब्ध आदेश:"
echo "संस्कृत-version"
echo "संस्कृत-compile"
echo "संस्कृत-install"
echo "चलाओ"
echo "स्थापन"
echo ""
echo "सूत्र-तंत्र उपयोग हेतु तैयार"
echo "====================================="
