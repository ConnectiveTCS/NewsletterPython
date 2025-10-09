"""
Test Arabic text handling
"""
import sys
import locale

# Test Arabic text
arabic_names = [
    "محمد الأحمد",
    "صالح بن محمد", 
    "فاطمة الزهراء",
    "عبدالله الرشيد"
]

print("System encoding:", sys.getdefaultencoding())
print("Locale:", locale.getdefaultlocale())
print()

print("Testing Arabic text handling:")
for name in arabic_names:
    print(f"Original: {repr(name)}")
    print(f"Display:  {name}")
    print(f"UTF-8:    {name.encode('utf-8')}")
    print()

# Test CSV-like scenario
csv_content = "email;name\ntest@example.com;محمد الأحمد\ntest2@example.com;صالح بن محمد"
print("CSV content:")
print(repr(csv_content))
print()
print("CSV display:")
print(csv_content)