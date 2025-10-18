# Campaign Archive & Delete Feature

## Overview
Added functionality to archive and delete campaigns in the Newsletter application.

## Features Added

### 1. Database Changes
- Added `is_archived` (Boolean) field to Campaign model
- Added `archived_at` (DateTime) field to Campaign model
- Created database migration with proper default values for SQLite compatibility

### 2. New Routes

#### Archive Campaign
- **Route**: `/campaigns/<id>/archive` (POST)
- **Function**: Archives a campaign
- Sets `is_archived = True` and records `archived_at` timestamp
- Redirects to campaigns list with success message

#### Unarchive Campaign
- **Route**: `/campaigns/<id>/unarchive` (POST)
- **Function**: Restores an archived campaign
- Sets `is_archived = False` and clears `archived_at`
- Redirects to archived campaigns list

#### Delete Campaign
- **Route**: `/campaigns/<id>/delete` (POST)
- **Function**: Permanently deletes a campaign
- Removes campaign and all associated email logs (cascade delete)
- Shows confirmation dialog before deletion
- Redirects to campaigns list with success message

### 3. User Interface Updates

#### Campaigns List Page (`campaigns.html`)
- Added "Archived" button to toggle between active and archived campaigns
- Shows "Active Campaigns" when viewing archived campaigns
- Archive button for each campaign (converts to Unarchive when viewing archived)
- Delete button for each campaign with confirmation dialog
- Updated page title to show "Archived Email Campaigns" when applicable

#### Campaign Detail Page (`campaign_detail.html`)
- Added "Archived" badge to campaign title when archived
- Added Archive/Unarchive button in Actions section
- Added Delete button with confirmation dialog
- Separated action buttons with horizontal rule for clarity

### 4. Functionality

#### View Active Campaigns (Default)
- URL: `/campaigns`
- Shows only campaigns where `is_archived = False`
- Displays Archive and Delete buttons for each campaign

#### View Archived Campaigns
- URL: `/campaigns?show_archived=true`
- Shows only campaigns where `is_archived = True`
- Displays Unarchive and Delete buttons for each campaign
- Shows link to return to active campaigns

#### Confirmation Dialogs
- Archive: "Are you sure you want to archive this campaign?"
- Unarchive: "Are you sure you want to unarchive this campaign?"
- Delete: "Are you sure you want to permanently delete this campaign? This action cannot be undone."

## Usage

### To Archive a Campaign:
1. Navigate to Campaigns list or Campaign detail page
2. Click the "Archive" button
3. Confirm the action
4. Campaign is moved to archived status

### To View Archived Campaigns:
1. Navigate to Campaigns list
2. Click "Archived" button in the header
3. View all archived campaigns

### To Unarchive a Campaign:
1. Navigate to Archived campaigns view
2. Click "Unarchive" button on desired campaign
3. Confirm the action
4. Campaign returns to active status

### To Delete a Campaign:
1. Navigate to Campaigns list or Campaign detail page
2. Click "Delete" button
3. Confirm the permanent deletion
4. Campaign and all related data are removed

## Technical Details

### Database Migration
- Migration file: `815fe2375955_add_is_archived_and_archived_at_to_.py`
- Uses `server_default='0'` for SQLite compatibility
- Adds index on `is_archived` for query performance

### Security
- All actions use POST method to prevent CSRF attacks
- Confirmation dialogs prevent accidental actions
- Database transactions with rollback on error

### Cascade Behavior
- Deleting a campaign automatically deletes all associated EmailLog records
- Prevents orphaned data in the database

## Benefits
1. **Organization**: Keep campaign list clean by archiving old campaigns
2. **Data Retention**: Archived campaigns are preserved for historical reference
3. **Flexibility**: Easy restoration of archived campaigns if needed
4. **Clean-up**: Permanent deletion option for campaigns no longer needed
5. **User Safety**: Confirmation dialogs prevent accidental deletions
