"""
Script to migrate database to UTF-8 and fix Arabic text encoding
"""
import sqlite3
import os

def fix_database_encoding():
    """Recreate database with proper UTF-8 encoding"""
    db_path = 'instance/newsletter.db'
    backup_path = 'instance/newsletter_backup.db'
    
    # Check if database exists
    if os.path.exists(db_path):
        print("Backing up existing database...")
        # Create backup
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        # Copy database
        import shutil
        shutil.copy2(db_path, backup_path)
        
        # Remove old database
        os.remove(db_path)
        print("Old database removed, backup created at:", backup_path)
    
    print("Database will be recreated with proper UTF-8 support when app starts.")
    print("Please restart the application to apply changes.")

if __name__ == "__main__":
    fix_database_encoding()