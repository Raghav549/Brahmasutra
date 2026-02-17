# ब्रह्म_आर्किटेक्चर_निर्माता.py
# BRAHMA ARCHITECTURE GENERATOR
# VERSION 127

class ब्रह्मआर्किटेक्चरनिर्माता:

    def __init__(self):

        print("ब्रह्म आर्किटेक्चर निर्माता सक्रिय")


    def निर्माण(self, analysis):

        architecture = {

            "frontend": False,
            "backend": False,
            "database": False,
            "ai_engine": False,
            "deployment": False,
            "api": False

        }

        if analysis.get("app") or analysis.get("website"):

            architecture["frontend"] = True
            architecture["backend"] = True
            architecture["database"] = True

        if analysis.get("ai"):

            architecture["ai_engine"] = True

        if analysis.get("backend"):

            architecture["backend"] = True

        if analysis.get("frontend"):

            architecture["frontend"] = True

        if analysis.get("database"):

            architecture["database"] = True

        if analysis.get("deployment") or analysis.get("cloud"):

            architecture["deployment"] = True

        if analysis.get("api") or analysis.get("backend"):

            architecture["api"] = True

        return architecture
