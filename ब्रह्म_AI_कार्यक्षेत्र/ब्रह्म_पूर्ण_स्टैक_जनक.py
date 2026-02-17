# ब्रह्म पूर्ण स्टैक जनक
# VERSION 124

import os

from ब्रह्म_HTML_जनक import ब्रह्मHTMLजनक
from ब्रह्म_स्वतः_बैकएंड_जनक import ब्रह्मस्वतःबैकएंडजनक


class ब्रह्मपूर्णस्टैकजनक:

    def __init__(self, workspace):

        self.workspace = workspace

        print("ब्रह्म पूर्ण स्टैक जनक सक्रिय")


    def जनन(self, app_name):

        print("पूर्ण ऐप जनन प्रारंभ:", app_name)

        app_dir = os.path.join(self.workspace, app_name)

        frontend_dir = os.path.join(app_dir, "frontend")

        backend_dir = os.path.join(app_dir, "backend")

        os.makedirs(frontend_dir, exist_ok=True)

        os.makedirs(backend_dir, exist_ok=True)


        # Generate frontend
        html_engine = ब्रह्मHTMLजनक(frontend_dir)

        html_engine.जनन(app_name)


        # Generate backend
        backend_engine = ब्रह्मस्वतःबैकएंडजनक(app_dir)

        backend_engine.जनन(app_name)


        print("पूर्ण स्टैक ऐप तैयार:", app_dir)

        return app_dir
