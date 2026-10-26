# 🕉️ ब्रह्म सार्वभौम प्रमाणीकरण निर्माता VERSION 37

import os
import json
import uuid

class ब्रह्मAUTHनिर्माता:

    def __init__(self):
        print("🕉️ ब्रह्म AUTH निर्माता सक्रिय")

        self.आधार = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_AUTH")
        self.उपयोगकर्ता_संचिका = os.path.join(self.आधार, "उपयोगकर्ता.json")

        os.makedirs(self.आधार, exist_ok=True)

        if not os.path.exists(self.उपयोगकर्ता_संचिका):
            with open(self.उपयोगकर्ता_संचिका, "w", encoding="utf-8") as f:
                json.dump({}, f)


    def उपयोगकर्ता_पढ़ो(self):

        with open(self.उपयोगकर्ता_संचिका, "r", encoding="utf-8") as f:
            return json.load(f)


    def उपयोगकर्ता_लिखो(self, data):

        with open(self.उपयोगकर्ता_संचिका, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


    def पंजीकरण(self, नाम, कूटशब्द):

        data = self.उपयोगकर्ता_पढ़ो()

        if नाम in data:
            print("त्रुटि: उपयोगकर्ता पहले से मौजूद")
            return None

        token = str(uuid.uuid4())

        data[नाम] = {
            "कूटशब्द": कूटशब्द,
            "टोकन": token
        }

        self.उपयोगकर्ता_लिखो(data)

        print("सफल पंजीकरण:", नाम)
        print("टोकन:", token)

        return token


    def प्रवेश(self, नाम, कूटशब्द):

        data = self.उपयोगकर्ता_पढ़ो()

        if नाम not in data:
            print("त्रुटि: उपयोगकर्ता नहीं मिला")
            return None

        if data[नाम]["कूटशब्द"] != कूटशब्द:
            print("त्रुटि: गलत कूटशब्द")
            return None

        token = str(uuid.uuid4())
        data[नाम]["टोकन"] = token

        self.उपयोगकर्ता_लिखो(data)

        print("सफल प्रवेश:", नाम)
        print("टोकन:", token)

        return token


    def सत्यापन(self, token):

        data = self.उपयोगकर्ता_पढ़ो()

        for user in data:

            if data[user]["टोकन"] == token:

                print("सत्यापित उपयोगकर्ता:", user)
                return True

        print("अमान्य टोकन")
        return False


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    global auth, t
    auth = ब्रह्मAUTHनिर्माता()

    print("\n--- परीक्षण ---")

    t = auth.पंजीकरण("देव", "123")

    auth.प्रवेश("देव", "123")

    auth.सत्यापन(t)


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
