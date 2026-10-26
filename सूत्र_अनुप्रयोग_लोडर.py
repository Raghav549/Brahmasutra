import zipfile
import json
import os

from सूत्र_कार्य_निष्पादक import कार्यनिष्पादक

class अनुप्रयोगलोडर:

    def निष्पादन(self, अनुप्रयोगसंचिका):

        आधार = os.path.expanduser("~/सूत्र-तंत्र/temp_app")

        if os.path.exists(आधार):

            for f in os.listdir(आधार):
                os.remove(आधार+"/"+f)

        else:
            os.makedirs(आधार)

        with zipfile.ZipFile(अनुप्रयोगसंचिका,"r") as zipf:

            zipf.extractall(आधार)

        manifest_path = आधार + "/manifest.json"

        with open(manifest_path,"r",encoding="utf-8") as f:

            manifest = json.load(f)

        main_file = आधार + "/" + manifest["मुख्य"]

        print("अनुप्रयोग प्रारम्भ:", manifest["नाम"])

        executor = कार्यनिष्पादक()

        executor.निष्पादन(main_file)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():

    print("🕉️ सूत्र अनुप्रयोग लोडर सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
