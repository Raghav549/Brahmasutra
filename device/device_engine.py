class उपकरण_प्रबन्धक:


    def __init__(self):

        self.उपकरणानि = {}



    def पञ्जीकरण(self, नाम):

        self.उपकरणानि[नाम] = "सक्रिय"

        print("उपकरण पञ्जीकृतः:", नाम)



    def सूची(self):

        print("उपकरण-सूची:")

        for d in self.उपकरणानि:

            print("-", d)



    def पठन(self, नाम):

        if नाम in self.उपकरणानि:

            print("उपकरणात् पठनं क्रियते:", नाम)

        else:

            print("उपकरणं न लब्धम्")



    def लेखन(self, नाम):

        if नाम in self.उपकरणानि:

            print("उपकरणे लेखनं क्रियते:", नाम)

        else:

            print("उपकरणं न लब्धम्")
