"""पुराना नाम — अब :mod:`brahma_auto` पर निर्देशित।

यह फ़ाइल पहले स्वतंत्र रूप से Flask ऐप बनाती थी और आयात करते ही
``input()`` पर अटक जाती थी। अब सारा तर्क ``brahma_auto.py`` में है; यह केवल
पुराने नाम को काम करता रखने के लिए है।
"""

from brahma_auto import create_app, main, safe_app_name  # noqa: F401

__all__ = ["create_app", "main", "safe_app_name"]


if __name__ == "__main__":
    raise SystemExit(main())
