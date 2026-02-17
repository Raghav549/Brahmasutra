# सूत्र तंत्र — Desktop Environment

print("सूत्र Desktop आरम्भ")



# apps
अनुप्रयोग = []



# files
सञ्चिका = {}



# open app
def अनुप्रयोग_आरम्भ(नाम):

    अनुप्रयोग.append(नाम)

    print("अनुप्रयोग आरम्भ:", नाम)



# list apps
def अनुप्रयोग_सूची():

    print("सक्रिय अनुप्रयोग:")

    for app in अनुप्रयोग:

        print(app)



# create file
def सञ्चिका_निर्माण(नाम, सामग्री):

    सञ्चिका[नाम] = सामग्री

    print("सञ्चिका निर्मित:", नाम)



# read file
def सञ्चिका_पठन(नाम):

    if नाम in सञ्चिका:

        print("सामग्री:", सञ्चिका[नाम])

    else:

        print("सञ्चिका नहीं मिली")



# show desktop
def desktop():

    print("सूत्र Desktop सक्रिय")



# test
if __name__ == "__main__":

    desktop()

    अनुप्रयोग_आरम्भ("calculator")

    अनुप्रयोग_आरम्भ("editor")

    अनुप्रयोग_सूची()

    सञ्चिका_निर्माण("test.txt", "नमस्ते सूत्र")

    सञ्चिका_पठन("test.txt")
