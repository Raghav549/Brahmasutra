# सूत्रभाषा Interpreter

print("🕉️ सूत्रभाषा सक्रिय")

while True:
    आदेश = input("सूत्र >>> ")

    if आदेश.startswith("प्रदर्शय"):
        text = आदेश.replace("प्रदर्शय", "").strip()
        print(text)

    elif आदेश.startswith("उद्घाटय"):
        app = आदेश.replace("उद्घाटय", "").strip()
        print(f"{app} उद्घाटित")

    elif आदेश.startswith("निर्गच्छ"):
        print("सूत्रभाषा समाप्त")
        break

    else:
        print("अज्ञात आदेश")
