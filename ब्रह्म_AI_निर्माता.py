# 🕉️ ब्रह्म AI निर्माता VERSION 7
# Prompt based generator

import os

class ब्रह्मAIनिर्माता:

    def __init__(self):

        print("🕉️ ब्रह्म AI निर्माता VERSION 7 सक्रिय")

        self.folder = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्रम")

        os.makedirs(self.folder, exist_ok=True)


    def विश्लेषण(self, prompt):

        prompt = prompt.lower()

        features = []

        if "chat" in prompt:
            features += ["लॉगिन", "उपयोगकर्ता", "चैट", "संदेश"]

        if "saas" in prompt:
            features += ["लॉगिन", "डेटाबेस", "API", "डैशबोर्ड", "सदस्यता"]

        if "api" in prompt:
            features += ["API", "डेटाबेस", "सर्वर"]

        if "app" in prompt:
            features += ["लॉगिन", "डैशबोर्ड"]

        if len(features) == 0:
            features += ["लॉगिन"]

        return list(set(features))


    def निर्माण(self, name, prompt):

        path = os.path.join(self.folder, name + ".ब्रह्म")

        features = self.विश्लेषण(prompt)

        code = []

        for f in features:
            code.append("स्थापित " + f + " 1")

        for f in features:
            code.append("दर्शय " + f)

        with open(path, "w", encoding="utf-8") as file:

            for line in code:
                file.write(line + "\n")

        print("AI कार्यक्रम निर्मित:", path)

        return path


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global ai, name, prompt
    ai = ब्रह्मAIनिर्माता()

    name = input("कार्यक्रम नाम: ")

    prompt = input("Prompt लिखें: ")

    ai.निर्माण(name, prompt)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
