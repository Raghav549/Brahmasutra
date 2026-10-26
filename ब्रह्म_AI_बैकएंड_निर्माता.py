"""ब्रह्म बैकएंड निर्माता — मानक-लाइब्रेरी सर्वर बनाता है।

पहले यह Flask कोड लिखता था जो बिना Flask के चल ही नहीं सकता था; अब
:mod:`brahma_templates` का स्व-निहित (self-contained) सर्वर लिखा जाता है।
"""

import os

from brahma_templates import write_chat_server


class ब्रह्मबैकएंडनिर्माता:

    def __init__(self):
        print("🕉️ ब्रह्म बैकएंड निर्माता सक्रिय")

    def निर्माण(self, app_name):

        base = os.path.expanduser(
            f"~/सूत्र-तंत्र/ब्रह्म_AI_अनुप्रयोग/{app_name}/backend"
        )

        os.makedirs(base, exist_ok=True)

        path = write_chat_server(base, app_name)

        print("Backend निर्मित:", path)

        return path
