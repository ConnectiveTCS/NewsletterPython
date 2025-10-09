# Arabic Names CSV Issue - Solution Guide

## Problem
The CSV file contains Arabic names that appear as question marks (???) instead of proper Arabic text. This happens when:

1. The original data source didn't export Arabic text properly
2. The file was saved without UTF-8 encoding
3. Excel or another program converted Arabic characters to question marks

## Current CSV Status
Your `sample_subscribers (1).csv` file contains entries like:
```
2220009@uob.edu.om;??? ??? ??????? ?? ???? ?? ???? ????????
2220100@uob.edu.om;???? ??? ???? ?? ??????? ?? ???? ?????????
```

## Solutions

### Option 1: Fix the CSV File (Recommended)
1. **Get the original source data** with proper Arabic names
2. **Save as UTF-8 CSV**:
   - In Excel: File → Save As → CSV UTF-8 (Comma delimited) (*.csv)
   - In Google Sheets: File → Download → Comma Separated Values (.csv)
3. **Use semicolon delimiter** if needed for Arabic names

### Option 2: Manual Correction
1. Open the CSV in a text editor that supports UTF-8 (like Notepad++)
2. Replace the question mark entries with proper Arabic names
3. Save the file as UTF-8

### Option 3: Use the Current System
The newsletter app will now:
- Import emails successfully (emails are not affected)
- Mark corrupted names as "[Name needs manual correction]"
- Allow you to edit names later in the subscriber management interface

## Testing Arabic Support
The system now properly supports Arabic names when they are correctly encoded:

```csv
email;name
test@example.com;محمد الأحمد
test2@example.com;فاطمة الزهراء
```

## How to Export CSV with Arabic Names from Excel
1. Open Excel with your data
2. File → Save As
3. Choose "CSV UTF-8 (Comma delimited) (*.csv)"
4. **Important**: Don't use regular CSV format
5. The UTF-8 format preserves Arabic characters

## Verification
After importing, Arabic names should display correctly in the web interface as:
- محمد الأحمد
- فاطمة الزهراء
- صالح بن محمد

Instead of: ??? ??? ???????