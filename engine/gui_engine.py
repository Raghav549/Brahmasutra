import os

def gui_निर्माण(file):

    print("संस्कृत GUI निर्माण आरम्भ:")

    with open(file, "r", encoding="utf-8") as f:

        lines = f.readlines()


    output_dir = os.path.expanduser("~/सूत्र-तंत्र/gui_output")

    if not os.path.exists(output_dir):

        os.makedirs(output_dir)


    xml_file = os.path.join(output_dir, "layout.xml")


    xml = []

    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"')
    xml.append('android:orientation="vertical"')
    xml.append('android:layout_width="match_parent"')
    xml.append('android:layout_height="match_parent">')


    for line in lines:

        line = line.strip()

        if line.startswith("पाठ"):

            text = line.replace("पाठ", "").strip()

            xml.append(f'<TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="{text}" />')


        elif line.startswith("बटन"):

            text = line.replace("बटन", "").strip()

            xml.append(f'<Button android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="{text}" />')


    xml.append("</LinearLayout>")


    with open(xml_file, "w", encoding="utf-8") as f:

        f.write("\n".join(xml))


    print("GUI layout निर्मित:")
    print(xml_file)
