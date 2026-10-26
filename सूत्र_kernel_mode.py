# 🕉️ सूत्र Kernel Mode Controller


class सूत्रKernelMode:


    def __init__(self):

        print("🕉️ Kernel Mode सक्रिय")

        self.kernel_active = True


    def execute_kernel(self, task):

        print("Kernel executing task:", task)


    def status(self):

        return "KERNEL_ACTIVE"


# ---------------------------------------------------------------------------
# Module level helpers used by ``सूत्र_mode_test.py`` and the kernel.
# ---------------------------------------------------------------------------
_वर्तमान = None


def प्रारम्भ():
    """Enter (or return) the current kernel-mode controller."""
    global _वर्तमान
    if _वर्तमान is None:
        _वर्तमान = सूत्रKernelMode()
    return _वर्तमान


def स्थिति():
    return _वर्तमान.status() if _वर्तमान is not None else "KERNEL_INACTIVE"


def निष्पादन(कार्य):
    return प्रारम्भ().execute_kernel(कार्य)
