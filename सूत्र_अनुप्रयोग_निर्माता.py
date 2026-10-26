import os
import json
import zipfile

class अनुप्रयोगनिर्माता:

    def निर्मित(self, नाम, कार्यसंचिका):

        आधार = os.path.expanduser("~/सूत्र-तंत्र/अनुप्रयोग")

        if not os.path.exists(आधार):
            os.makedirs(आधार)

        अनुप्रयोग_पथ = आधार + "/" + नाम

        if not os.path.exists(अनुप्रयोग_पथ):
            os.makedirs(अनुप्रयोग_पथ)

        # copy executable
        लक्ष्य = अनुप्रयोग_पथ + "/main.कार्य"

        with open(कार्यसंचिका,"rb") as स्रोत:
            डेटा = स्रोत.read()

        with open(लक्ष्य,"wb") as लक्ष्यसंचिका:
            लक्ष्यसंचिका.write(डेटा)

        manifest = {
            "नाम": नाम,
            "संस्करण": "1.0",
            "मुख्य": "main.कार्य"
        }

        with open(अनुप्रयोग_पथ + "/manifest.json","w",encoding="utf-8") as f:
            json.dump(manifest,f,ensure_ascii=False,indent=4)

        zip_path = आधार + "/" + नाम + ".अनुप्रयोग"

        with zipfile.ZipFile(zip_path,"w") as zipf:

            for root, dirs, files in os.walk(अनुप्रयोग_पथ):

                for file in files:

                    full = os.path.join(root,file)

                    rel = os.path.relpath(full,अनुप्रयोग_पथ)

                    zipf.write(full,rel)

        print("अनुप्रयोग निर्मित:", zip_path)

        return zip_path


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    print("🕉️ सूत्र अनुप्रयोग निर्माता सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
