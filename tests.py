
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

print("result for current directory")
print(get_files_info("calculator", "."))

print("\nresult for 'pkg' direcotry")
print(get_files_info("calculator", "pkg"))

print("\nresult for '/bin' direcotry")
print(get_files_info("calculator", "/bin"))

print("\nresult for '../' direcotry")
print(get_files_info("calculator", "../"))

print("testing the get file_content")
print(get_file_content("calculator", "main.py"))

print(get_file_content("calculator", "lorem.txt"))
