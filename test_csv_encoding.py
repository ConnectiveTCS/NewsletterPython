"""
Test reading the actual CSV file to check Arabic encoding
"""
import csv
import io

def test_csv_file(file_path):
    """Test reading CSV file with different encodings"""
    
    encodings_to_try = ['utf-8-sig', 'utf-8', 'utf-16', 'cp1256', 'latin1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            print(f"\n=== Testing with encoding: {encoding} ===")
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                
            print(f"File read successfully with {encoding}")
            
            # Check for Arabic characters in the content
            arabic_found = False
            for char in content:
                if '\u0600' <= char <= '\u06FF':
                    arabic_found = True
                    break
            
            print(f"Arabic characters found: {arabic_found}")
            
            # Parse as CSV
            stream = io.StringIO(content, newline=None)
            delimiter = ';' if ';' in content.split('\n')[0] else ','
            csv_reader = csv.reader(stream, delimiter=delimiter)
            
            print(f"Delimiter detected: '{delimiter}'")
            
            # Show first few rows
            row_count = 0
            for row in csv_reader:
                row_count += 1
                if row_count <= 10:  # Show first 10 rows
                    if len(row) >= 2:
                        email, name = row[0].strip(), row[1].strip()
                        
                        # Check if name contains Arabic
                        contains_arabic = any('\u0600' <= char <= '\u06FF' for char in name)
                        
                        print(f"Row {row_count}: {email} | {name} | Arabic: {contains_arabic}")
                        
                        if contains_arabic:
                            print(f"  Raw: {repr(name)}")
                
                if row_count >= 10:
                    break
            
            return encoding  # Return successful encoding
            
        except Exception as e:
            print(f"Failed with {encoding}: {e}")
    
    return None

# Test with the sample CSV file path
csv_file_path = r"C:\Users\Kyle\Downloads\sample_subscribers (1).csv"

print("Testing CSV file encoding...")
successful_encoding = test_csv_file(csv_file_path)

if successful_encoding:
    print(f"\n✅ Successfully read CSV with encoding: {successful_encoding}")
else:
    print(f"\n❌ Could not read CSV file with any encoding")