# 🎯 Newsletter Application - Quick Reference Guide

## 📧 Template Variables Reference Card

Copy and paste these into your email templates:

```html
<!-- Greeting -->
<h1>Hello {{first_name}},</h1>
<h2>Hi {{name}},</h2>

<!-- Personal Info -->
<p>Your email: {{email}}</p>

<!-- Date/Time -->
<p>Today: {{date}}</p>
<p>Year: {{year}}</p>

<!-- Campaign Info -->
<p>Campaign: {{campaign_name}}</p>

<!-- Required: Unsubscribe Link -->
<p style="text-align: center; color: #999; font-size: 12px;">
  <a href="{{unsubscribe_link}}">Unsubscribe</a>
</p>
```

---

## 🎨 Sample Email Templates

### Welcome Email
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #667eea; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { text-align: center; color: #999; font-size: 12px; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome {{first_name}}! 🎉</h1>
        </div>
        <div class="content">
            <p>Dear {{name}},</p>
            <p>Thank you for subscribing to our newsletter on {{date}}!</p>
            <p>We're excited to have you on board.</p>
            <p>You'll receive updates, tips, and exclusive content directly to {{email}}.</p>
        </div>
        <div class="footer">
            <p>Campaign: {{campaign_name}}</p>
            <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
```

### Newsletter Template
```html
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center;">
        <h1>Newsletter - {{date}} 📰</h1>
    </div>
    
    <div style="padding: 30px;">
        <h2>Hi {{first_name}},</h2>
        
        <h3>📌 This Week's Highlights</h3>
        <ul>
            <li>Update 1: Lorem ipsum dolor sit amet</li>
            <li>Update 2: Consectetur adipiscing elit</li>
            <li>Update 3: Sed do eiusmod tempor</li>
        </ul>
        
        <h3>💡 Featured Article</h3>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>
        <a href="#" style="background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0;">Read More</a>
        
        <h3>📢 Upcoming Events</h3>
        <p>Join us for our next webinar on [Date]!</p>
    </div>
    
    <div style="background: #f5f5f5; padding: 20px; text-align: center; color: #666; font-size: 12px;">
        <p>You're receiving this because you subscribed at {{email}}</p>
        <p>Campaign: {{campaign_name}} | {{year}}</p>
        <p><a href="{{unsubscribe_link}}" style="color: #666;">Unsubscribe</a></p>
    </div>
</body>
</html>
```

### Promotional Email
```html
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif;">
    <div style="max-width: 600px; margin: 0 auto; background: white;">
        <!-- Banner -->
        <div style="background: #ff6b6b; color: white; padding: 40px; text-align: center;">
            <h1 style="margin: 0; font-size: 36px;">🎁 Special Offer!</h1>
            <p style="font-size: 18px;">Just for You, {{first_name}}</p>
        </div>
        
        <!-- Content -->
        <div style="padding: 40px;">
            <h2>Dear {{name}},</h2>
            
            <p style="font-size: 16px; line-height: 1.6;">
                We have an exclusive offer just for our valued subscribers!
            </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-left: 4px solid #ff6b6b; margin: 20px 0;">
                <h3 style="margin: 0 0 10px 0;">50% OFF Everything!</h3>
                <p style="margin: 0; color: #666;">Valid until {{date}}</p>
            </div>
            
            <center>
                <a href="#" style="background: #ff6b6b; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; font-weight: bold; font-size: 16px;">
                    Shop Now →
                </a>
            </center>
            
            <p style="color: #666; font-size: 14px;">
                This offer is exclusively for you at {{email}}
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background: #2d3436; color: white; padding: 30px; text-align: center;">
            <p style="margin: 0 0 10px 0;">{{campaign_name}}</p>
            <p style="margin: 0; font-size: 12px; opacity: 0.7;">
                <a href="{{unsubscribe_link}}" style="color: white;">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>
```

---

## 📅 Scheduling Examples

### Schedule Format
Use this format in the scheduling form:
```
2025-10-18T14:30
```

### Common Schedules
```
Tomorrow 9 AM:     2025-10-19T09:00
Next Monday 8 AM:  2025-10-21T08:00
Weekend 6 PM:      2025-10-20T18:00
Next Month:        2025-11-01T10:00
```

---

## 🔗 API Endpoints Quick Reference

### Get Template Variables
```javascript
fetch('/api/template-variables')
  .then(r => r.json())
  .then(data => console.log(data));
```

### Get Campaign Status
```javascript
fetch('/api/campaign/1/status')
  .then(r => r.json())
  .then(data => {
    console.log('Status:', data.status);
    console.log('Sent:', data.total_sent);
    console.log('Failed:', data.total_failed);
  });
```

### Export Subscribers
```html
<a href="/subscribers/export" download>Export CSV</a>
```

---

## 🎨 CSS Styling Tips

### Responsive Email
```html
<style>
    @media only screen and (max-width: 600px) {
        .container { width: 100% !important; }
        .header { padding: 10px !important; }
        h1 { font-size: 24px !important; }
    }
</style>
```

### Buttons
```html
<a href="#" style="
    background: #667eea;
    color: white;
    padding: 12px 30px;
    text-decoration: none;
    border-radius: 5px;
    display: inline-block;
    font-weight: bold;
">Click Here</a>
```

### Cards
```html
<div style="
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
">
    <h3>Card Title</h3>
    <p>Card content goes here...</p>
</div>
```

---

## 📊 Workflow Examples

### Creating a Campaign
1. **Create Template**
   - Go to Templates → Add Template
   - Add subject with `{{first_name}}`
   - Add content with variables
   - Include `{{unsubscribe_link}}`
   - Save

2. **Create Campaign**
   - Go to Campaigns → Create Campaign
   - Enter campaign name
   - Select template
   - Save as draft

3. **Schedule or Send**
   - Option A: Click "Send Now"
   - Option B: Set date/time and click "Schedule"

### Importing Subscribers
1. Prepare CSV file:
   ```csv
   email,name
   john@example.com,John Doe
   jane@example.com,Jane Smith
   ```

2. Go to Subscribers → Import
3. Upload CSV file
4. System validates emails
5. Duplicates are skipped automatically

### Exporting Data
1. Go to Subscribers page
2. Click "Export" button
3. CSV downloads with all data
4. Open in Excel/Sheets

---

## 🛡️ Best Practices

### Email Templates
✅ Always include `{{unsubscribe_link}}`  
✅ Use `{{first_name}}` for personalization  
✅ Test with preview before sending  
✅ Keep content under 102KB  
✅ Use inline CSS styles  

### Campaign Scheduling
✅ Schedule at least 5 minutes ahead  
✅ Consider time zones  
✅ Test with small group first  
✅ Check subscriber count before sending  

### Subscriber Management
✅ Clean list regularly  
✅ Export backups monthly  
✅ Remove bounced emails  
✅ Respect unsubscribe requests  

---

## 🚨 Troubleshooting

### Emails Not Sending
```
1. Check SMTP settings in .env
2. Verify email credentials
3. Check campaign status
4. View campaign logs
5. Check error messages
```

### Scheduler Not Working
```
1. Restart application
2. Check scheduled_at time
3. Verify is_scheduled = True
4. Check scheduler logs
5. Cancel and reschedule
```

### Variables Not Replaced
```
1. Use {{ }} double braces
2. Check variable spelling
3. Test with test_features.py
4. Verify subscriber has data
```

---

## 📞 Quick Commands

```bash
# Start application
python run.py

# Run tests
python test_features.py

# Check database
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.inspect(db.engine).get_table_names()

# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Export subscribers
# Visit: http://localhost:5000/subscribers/export
```

---

## 🎯 Keyboard Shortcuts (Future)

Coming soon in UI:
- `Ctrl+S` - Save template
- `Ctrl+N` - New campaign
- `Ctrl+E` - Export subscribers
- `Esc` - Close modal

---

**Last Updated:** October 18, 2025  
**Version:** 2.0  
**Quick Help:** See FEATURES_IMPLEMENTATION.md for details
