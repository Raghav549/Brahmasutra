"""🕉️ सूत्र Boot Simulator — build, verify and boot a सूत्र image.

The demo used to read two *generated binaries* (``सूत्र.img`` and
``boot_kernel.bin``) that were committed with a stale, incompatible layout, and
then crashed in the OS loader.  It now assembles a kernel, packs a boot image,
verifies the header and boots it — no binary artefacts in the repository.
"""

import os
import tempfile

import brahma_bytecode
from सूत्र_os_loader import OSLoader

KERNEL_SOURCE = """संकल्प अ 50
संकल्प ब 70
योग अ ब
दर्शय अ
"""


def build_image(directory: str, source: str = KERNEL_SOURCE):
    """Assemble ``source`` and write ``directory/सूत्र.img``; return its path."""
    kernel = brahma_bytecode.assemble(source)
    image = brahma_bytecode.pack_image(kernel)
    path = os.path.join(directory, "सूत्र.img")
    with open(path, "wb") as handle:
        handle.write(image)
    return path


class BootSimulator:
    """A (pure-Python) boot sequence: verify the image, load the kernel, run it."""

    def __init__(self, image: str = "सूत्र.img", verbose: bool = True) -> None:
        self.image = image
        self.verbose = verbose
        if verbose:
            print("🕉️ सूत्र Boot Simulator प्रारम्भ")

    def boot(self):
        """Boot ``self.image``; return the kernel's register state."""
        if self.verbose:
            print("Boot image लोड हो रहा है...")
        try:
            with open(self.image, "rb") as handle:
                data = handle.read()
        except FileNotFoundError:
            print("image नहीं मिला:", self.image)
            return None

        try:
            version, kernel = brahma_bytecode.unpack_image(data)
        except brahma_bytecode.असेंबली_त्रुटि as exc:
            print("अमान्य image:", exc)
            return None

        if self.verbose:
            print("Version:", version)
            print("Kernel लोड सफल (%d बाइट)" % len(kernel))
            print("Kernel execute हो रहा है...")

        return OSLoader(verbose=self.verbose).चलाओ(kernel)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        image = build_image(tmp)
        BootSimulator(image).boot()
    return 0


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        main()
    else:
        raise SystemExit(_brahma_cli_run(main))
