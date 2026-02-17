#!/usr/bin/env bash

echo "सूत्र OS ISO निर्माण प्रारम्भ"

BASE=~/सूत्र-तंत्र/os
ISO=$BASE/iso
BOOT=$ISO/boot
GRUB=$BOOT/grub

mkdir -p $BOOT
mkdir -p $GRUB

echo "सूत्र kernel copy"
cp $BASE/kernel/sutra_kernel $BOOT/

echo "GRUB config निर्माण"
cat > $GRUB/grub.cfg << EOF
set timeout=0
set default=0

menuentry "सूत्र OS" {
    linux /boot/sutra_kernel
}
EOF

echo "ISO file निर्माण"
cd $BASE

tar -cvf सूत्र_os.iso iso >/dev/null 2>&1

echo "ISO सफल:"
echo "$BASE/सूत्र_os.iso"
