"""यन्त्र (bytecode machine) परीक्षण — device manager + interpreter demo.

The demo used to execute ``परीक्षण.यन्त्र``, a *generated* binary that was
committed to git and produced by an older, incompatible compiler — so the demo
failed with ``अज्ञात ऑपकोड``.  It now assembles ``परीक्षण.सूत्र`` on the fly into
a temporary file and executes that, so the repository holds only sources.
"""

import os
import tempfile

import सूत्र_यन्त्र_चालक as चालक
import सूत्र_यन्त्र_निष्पादक as यन्त्र
from सूत्र_संकलक import संकलक

स्रोत = os.path.join(os.path.dirname(os.path.abspath(__file__)), "परीक्षण.सूत्र")


def main():
    प्रबंधक = चालक.यन्त्रचालकतंत्र()

    प्रबंधक.पंजीकरण("संग्रहण")
    प्रबंधक.पंजीकरण("प्रदर्शन")
    प्रबंधक.पंजीकरण("कुंजीपटल")

    प्रबंधक.सक्रिय("संग्रहण")
    प्रबंधक.सक्रिय("प्रदर्शन")
    प्रबंधक.निष्क्रिय("संग्रहण")

    प्रबंधक.सूची()

    with tempfile.TemporaryDirectory() as tmp:
        लक्ष्य = os.path.join(tmp, "परीक्षण.यन्त्र")
        संकलक().संकलित(स्रोत, लक्ष्य)
        य = यन्त्र.सूत्रयन्त्र()
        य.चलाओ(लक्ष्य)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
