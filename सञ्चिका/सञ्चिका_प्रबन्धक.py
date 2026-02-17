import os


class सञ्चिका_प्रबन्धक:


    def __init__(self):

        self.मूलपथ = os.path.expanduser("~/सूत्र-तंत्र/सञ्चिका/संग्रह")

        if not os.path.exists(self.मूलपथ):

            os.makedirs(self.मूलपथ)

            print("सञ्चिका-संग्रह निर्मितः")



    def निर्माणम्(self, नाम):

        पथ = os.path.join(self.मूलपथ, नाम)

        with open(पथ, "w", encoding="utf-8") as f:

            f.write("")

        print("सञ्चिका निर्मिता:", नाम)



    def लेखनम्(self, नाम, विषय):

        पथ = os.path.join(self.मूलपथ, नाम)

        with open(पथ, "w", encoding="utf-8") as f:

            f.write(विषय)

        print("सञ्चिकायां लेखनं सम्पन्नम्:", नाम)



    def पठनम्(self, नाम):

        पथ = os.path.join(self.मूलपथ, नाम)

        if os.path.exists(पथ):

            with open(पथ, "r", encoding="utf-8") as f:

                विषय = f.read()

                print("सञ्चिका-पठनम्:", नाम)

                print(विषय)

        else:

            print("सञ्चिका नास्ति:", नाम)



    def सूची(self):

        सञ्चिकाः = os.listdir(self.मूलपथ)

        print("सञ्चिका-सूची:")

        for स in सञ्चिकाः:

            print("-", स)



    def विलोपनम्(self, नाम):

        पथ = os.path.join(self.मूलपथ, नाम)

        if os.path.exists(पथ):

            os.remove(पथ)

            print("सञ्चिका विलोपिता:", नाम)

        else:

            print("सञ्चिका नास्ति")
