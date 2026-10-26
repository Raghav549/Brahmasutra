

from ब्रह्म_CPU_कर्ण import ब्रह्मCPUकर्ण


class ब्रह्मप्रक्रियानिष्पादनकर्ण:


    def __init__(self):

        self.cpu = ब्रह्मCPUकर्ण()

        self.processes = {}

        self.pid_counter = 1


    def निर्माण(self, नाम, आदेशसूची):

        pid = self.pid_counter

        self.processes[pid] = {

            "नाम": नाम,
            "आदेश": आदेशसूची,
            "स्थिति": "तैयार"

        }

        self.pid_counter += 1

        print("प्रक्रिया निर्मित:", नाम, "PID:", pid)

        return pid


    def निष्पादन(self, pid):

        if pid not in self.processes:

            print("त्रुटि: प्रक्रिया नहीं मिली")

            return


        process = self.processes[pid]

        print("प्रक्रिया निष्पादन प्रारम्भ:", process["नाम"])

        process["स्थिति"] = "चल रहा"


        for आदेश in process["आदेश"]:

            self.आदेश_चलाओ(आदेश)


        process["स्थिति"] = "समाप्त"

        print("प्रक्रिया समाप्त:", process["नाम"])


    def आदेश_चलाओ(self, आदेश):

        भाग = आदेश.split()


        if भाग[0] == "स्थापित":

            नाम = भाग[1]
            मान = int(भाग[2])

            self.cpu.स्थापित(नाम, मान)


        elif भाग[0] == "योग":

            अ = भाग[1]
            ब = भाग[2]

            self.cpu.योग(अ, ब)


        elif भाग[0] == "दर्शय":

            नाम = भाग[1]

            print("मान:", नाम, "=", self.cpu.प्राप्त(नाम))


        else:

            print("अमान्य आदेश:", आदेश)


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("🕉️ ब्रह्म प्रक्रिया निष्पादन कर्ण सक्रिय")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
