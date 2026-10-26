# 🕉️ सूत्र शेल v2 — पूर्ण स्वदेशी शेल


def प्रारम्भ(interactive=None):
    """Start the shell; without a terminal it reports ready instead of blocking."""

    import sys

    print("🕉️ सूत्र शेल v2 सक्रिय")

    if interactive is None:
        interactive = bool(sys.stdin and sys.stdin.isatty())

    if not interactive:
        print("🕉️ शेल तैयार (इंटरैक्टिव नहीं)")
        return None

    while True:

        try:

            आदेश = input("सूत्र >>> ")

            if आदेश == "निर्गम":

                print("शेल बन्द")
                break


            elif आदेश == "स्थिति":

                print("प्रणाली सक्रिय")


            elif आदेश == "स्मृति":

                print("स्मृति सक्रिय")


            elif आदेश == "प्रक्रिया":

                print("प्रक्रिया सक्रिय")


            elif आदेश == "सञ्चिका":

                print("सञ्चिका तंत्र सक्रिय")


            elif आदेश == "यन्त्र":

                print("यन्त्र तंत्र सक्रिय")


            else:

                print("अज्ञात आदेश:", आदेश)


        except KeyboardInterrupt:

            print("\nशेल बन्द")
            break
