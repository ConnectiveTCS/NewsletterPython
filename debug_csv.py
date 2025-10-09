import csv
import io
import re

def format_name(name):
    """
    Format names properly:
    - Arabic names: keep as-is (preserve original formatting)
    - English names: Title Case (First Letter Capital, rest lowercase)
    - Handle special cases like hyphenated names, apostrophes, etc.
    """
    if not name or not name.strip():
        return ""
    
    name = name.strip()
    
    # Check if name contains Arabic characters
    def contains_arabic(text):
        for char in text:
            if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF':
                return True
        return False
    
    # If name contains Arabic characters, preserve original formatting
    if contains_arabic(name):
        return name
    
    # For non-Arabic names, apply proper title casing
    formatted_name = []
    name_parts = name.split()
    
    for part in name_parts:
        if not part:
            continue
            
        # Handle hyphenated names (e.g., "Al-Rashid")
        if '-' in part:
            hyphen_parts = part.split('-')
            formatted_hyphen = []
            for hyp_part in hyphen_parts:
                if hyp_part:
                    if hyp_part.lower() in ['al', 'de', 'van', 'von', 'da', 'del', 'della', 'di']:
                        formatted_hyphen.append(hyp_part.title())
                    else:
                        formatted_hyphen.append(hyp_part.capitalize())
            formatted_name.append('-'.join(formatted_hyphen))
        
        # Handle names with apostrophes (e.g., "O'Connor")
        elif "'" in part:
            apos_parts = part.split("'")
            formatted_apos = []
            for apos_part in apos_parts:
                if apos_part:
                    formatted_apos.append(apos_part.capitalize())
                else:
                    formatted_apos.append(apos_part)
            formatted_name.append("'".join(formatted_apos))
        
        # Handle regular names
        else:
            if part.lower() in ['al', 'de', 'van', 'von', 'da', 'del', 'della', 'di']:
                formatted_name.append(part.title())
            # Handle Celtic names like McPherson, MacDonald
            elif part.lower().startswith('mc') and len(part) > 2:
                formatted_name.append('Mc' + part[2:].capitalize())
            elif part.lower().startswith('mac') and len(part) > 3:
                formatted_name.append('Mac' + part[3:].capitalize())
            else:
                formatted_name.append(part.capitalize())
    
    return ' '.join(formatted_name)

def test_csv_parsing(csv_content):
    """Test CSV parsing with the same logic as the app"""
    print(f"Raw CSV content (first 200 chars): {repr(csv_content[:200])}")
    
    # Detect delimiter (tab, semicolon, or comma)
    sample_line = csv_content.split('\n')[0] if '\n' in csv_content else csv_content
    
    # Check for tab delimiter first (most specific)
    if '\t' in sample_line:
        delimiter = '\t'
        delimiter_name = 'tab'
    # Then check for semicolon vs comma
    elif ';' in sample_line and sample_line.count(';') > sample_line.count(','):
        delimiter = ';'
        delimiter_name = 'semicolon'
    else:
        delimiter = ','
        delimiter_name = 'comma'
    
    print(f"Detected delimiter: '{delimiter_name}' ({repr(delimiter)})")
    
    stream = io.StringIO(csv_content, newline=None)
    csv_input = csv.reader(stream, delimiter=delimiter)
    
    valid_count = 0
    invalid_count = 0
    row_number = 0
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    for row in csv_input:
        row_number += 1
        print(f"Row {row_number}: {row}")
        
        # Skip empty rows
        if not row or (len(row) == 1 and not row[0].strip()):
            print("  -> Skipped (empty)")
            continue
        
        # Check if this looks like a header row
        if row_number == 1:
            row_str = ','.join(row).lower()
            if 'email' in row_str or 'e-mail' in row_str:
                print("  -> Skipped (header)")
                continue
        
        if len(row) >= 1:
            email = row[0].strip()
            name = row[1].strip() if len(row) > 1 else ''
            
            # Clean up email
            email = email.replace('"', '').replace("'", "").strip().lower()
            
            # Format name properly
            formatted_name = format_name(name)
            
            print(f"  -> Processing: email='{email}', name='{name}' -> formatted='{formatted_name}'")
            
            if email and re.match(email_pattern, email):
                valid_count += 1
                print(f"  -> VALID")
            else:
                invalid_count += 1
                print(f"  -> INVALID (doesn't match pattern)")
    
    print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")
    return valid_count, invalid_count

# Test with sample data
sample_csv = """email,name
john@example.com,John Doe
jane@example.com,Jane Smith
bob@company.com,Bob Johnson"""

print("Testing sample CSV:")
test_csv_parsing(sample_csv)

# Test with semicolon-separated data (like user's file)
semicolon_csv = """email;name
24f026@otc.edu.om;Maryam Alsidairi
kirubhashini@iswkoman.com;Kirubhashini
veeranka.shah@iswkoman.com;Veeranka Shah"""

print("\nTesting semicolon-separated CSV:")
test_csv_parsing(semicolon_csv)

# Test with tab-separated data (like user's actual file)
tab_csv = """email	name
24f026@otc.edu.om	Maryam Alsidairi
kirubhashini@iswkoman.com	Kirubhashini
sima4french@gmail.com	SIMA GHOSH DASTIDAR"""

print("\nTesting tab-separated CSV:")
test_csv_parsing(tab_csv)

print("\n" + "="*50)
print("Testing name formatting:")

# Test various name formats
test_names = [
    "JOHN DOE",  # All caps
    "jane smith",  # All lowercase  
    "Bob O'Connor",  # Apostrophe
    "Al-Rashid",  # Hyphenated
    "MARY JANE WATSON",  # Multiple names all caps
    "de la Cruz",  # Prefix
    "محمد الأحمد",  # Arabic name
    "صالح بن محمد",  # Arabic name
    "SIMA GHOSH DASTIDAR",  # Mixed case
    "Kyle McPherson"  # Already formatted
]

for name in test_names:
    formatted = format_name(name)
    print(f"'{name}' -> '{formatted}'")

print("\n" + "="*50)
print("Please check your CSV file format!")