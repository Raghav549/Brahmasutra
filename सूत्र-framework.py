# सूत्र तंत्र — Application Framework




# app registry
अनुप्रयोग_पंजी = {}



# install app
def अनुप्रयोग_स्थापय(नाम, कार्य):

    अनुप्रयोग_पंजी[नाम] = कार्य

    print("अनुप्रयोग स्थापित:", नाम)



# run app
def अनुप्रयोग_चलाय(नाम):

    if नाम in अनुप्रयोग_पंजी:

        print("अनुप्रयोग चल रहा:", नाम)

        अनुप्रयोग_पंजी[नाम]()

    else:

        print("अनुप्रयोग नहीं मिला")



# example app
def गणक():

    print("गणक आरम्भ")

    अ = 5

    ब = 7

    print("योग:", अ + ब)



# example app
def नमस्ते():

    print("नमस्ते! सूत्र OS में आपका स्वागत है")


# ---------------------------------------------------------------------------
# Demo body. Moved behind a __main__ guard by tools/harden_imports.py so that
# importing this module has no side effects. Classes and functions above stay
# at module level, so the module's public names are unchanged.
# ---------------------------------------------------------------------------
def _main():
    print("सूत्र Application Framework आरम्भ")
    अनुप्रयोग_स्थापय("गणक", गणक)

    अनुप्रयोग_स्थापय("नमस्ते", नमस्ते)

    अनुप्रयोग_चलाय("गणक")

    अनुप्रयोग_चलाय("नमस्ते")


if __name__ == "__main__":
    try:
        from brahma_cli import चलाओ as _brahma_cli_run
    except ImportError:  # script copied outside the repository
        _main()
    else:
        raise SystemExit(_brahma_cli_run(_main))
