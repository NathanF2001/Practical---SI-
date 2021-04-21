import os

file = "dummyfile02-with-a-bigger-name-to-test-your-buffer-treatment.txt"

file_s = os.stat(file).st_size
print(file_s)

tes = open(file, "rb")
data = tes.read()
print(data)
print(len(data))
