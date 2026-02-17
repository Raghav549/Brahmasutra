from सूत्र_अनुसूचक import सूत्रअनुसूचक


def कार्य१():

    print("ऐप१ चल रहा है")


def कार्य२():

    print("ऐप२ चल रहा है")


def कार्य३():

    print("ऐप३ चल रहा है")


scheduler = सूत्रअनुसूचक()

scheduler.जोड़("ऐप१", कार्य१)

scheduler.जोड़("ऐप२", कार्य२)

scheduler.जोड़("ऐप३", कार्य३)


scheduler.चलाओ()
