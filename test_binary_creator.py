data = bytearray()

# LOAD अ 10
data.append(1)
data.append(ord("अ"))
data += (10).to_bytes(4,"big")

# LOAD ब 20
data.append(1)
data.append(ord("ब"))
data += (20).to_bytes(4,"big")

# ADD अ ब
data.append(2)
data.append(ord("अ"))
data.append(ord("ब"))

# SHOW अ
data.append(3)
data.append(ord("अ"))

# END
data.append(4)

with open("test.सूत्रबिन","wb") as f:
    f.write(data)

print("Binary created")
