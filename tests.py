
from functions.get_files_info import get_files_info

print("result for current directory")
print(get_files_info("calulator", "."))

print("\nresult for 'pkg' direcotry")
print(get_files_info("calculator", "pkg"))

print("\nresult for '/bin' direcotry")
print(get_files_info("calculator", "/bin"))

print("\nresult for '../' direcotry")
print(get_files_info("calculator", "../"))
