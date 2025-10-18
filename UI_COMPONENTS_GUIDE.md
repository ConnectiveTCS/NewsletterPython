# UI/UX Components Quick Reference

## 🎨 Design System Quick Guide

Quick reference for developers working on the Newsletter application UI.

---

## Color Palette

```css
/* Primary Colors */
--fb-blue: #1877f2;           /* Primary actions, links */
--fb-blue-dark: #166fe5;      /* Hover states */

/* Backgrounds */
--fb-bg: #f0f2f5;             /* Page background */
--fb-card: #ffffff;           /* Card background */
--fb-hover: #f2f3f5;          /* Hover background */

/* Borders & Text */
--fb-border: #e4e6eb;         /* Borders, dividers */
--fb-text: #050505;           /* Primary text */
--fb-text-secondary: #65676b; /* Secondary text */
```

### Usage Examples
```css
/* Primary Button */
background-color: var(--fb-blue);

/* Card Background */
background-color: var(--fb-card);
border: 1px solid var(--fb-border);
```

---

## Typography

### Font Families
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             Helvetica, Arial, sans-serif;
```

### Font Sizes
```css
/* Headings */
h1 { font-size: 2.5rem; font-weight: 700; }
h2 { font-size: 2rem; font-weight: 700; }
h3 { font-size: 1.75rem; font-weight: 700; }
h4 { font-size: 1.5rem; font-weight: 700; }
h5 { font-size: 1.25rem; font-weight: 600; }

/* Statistics */
.card-stat h5 { font-size: 2.5rem; font-weight: bold; }

/* Body Text */
p { font-size: 1rem; line-height: 1.6; }

/* Small Text */
.form-text { font-size: 0.875rem; }
```

### Font Weights
```css
/* Regular */
font-weight: 400;

/* Medium (labels, navigation) */
font-weight: 500;

/* Semi-Bold (form labels, buttons) */
font-weight: 600;

/* Bold (headings) */
font-weight: 700;
```

---

## Spacing System

```css
/* Base spacing unit: 1rem = 16px */

/* Small gaps */
gap: 0.5rem;        /* 8px */
padding: 0.5rem;    /* 8px */

/* Medium spacing */
gap: 1rem;          /* 16px */
padding: 1rem;      /* 16px */

/* Large spacing */
gap: 1.5rem;        /* 24px */
padding: 2rem;      /* 32px */

/* Extra large */
padding: 3rem;      /* 48px - empty states */
```

### Common Patterns
```css
/* Card padding */
.card-body { padding: 1.25rem; }

/* Form groups */
.mb-3 { margin-bottom: 1rem; }

/* Section spacing */
.mb-4 { margin-bottom: 1.5rem; }

/* Empty states */
.empty-state { padding: 3rem 1rem; }
```

---

## Border Radius

```css
/* Small (buttons, inputs) */
border-radius: 6px;

/* Medium (cards) */
border-radius: 8px;

/* Large (badges) */
border-radius: 12px;

/* Pill (full rounded) */
border-radius: 50px;
```

---

## Buttons

### Button Styles
```html
<!-- Primary Action -->
<button class="btn btn-primary">
    <i class="fas fa-plus"></i> Create
</button>

<!-- Secondary Action -->
<button class="btn btn-secondary">Cancel</button>

<!-- Danger Action -->
<button class="btn btn-danger">
    <i class="fas fa-trash"></i> Delete
</button>

<!-- Outline Style -->
<button class="btn btn-outline-primary">View</button>

<!-- Large Button -->
<button class="btn btn-primary btn-lg">Get Started</button>

<!-- Small Button -->
<button class="btn btn-primary btn-sm">Edit</button>
```

### Button with Loading State
```html
<button type="submit" class="btn btn-primary" id="submitBtn">
    <span class="btn-text">Submit</span>
</button>

<script>
form.addEventListener('submit', function(e) {
    submitBtn.classList.add('btn-loading');
    submitBtn.disabled = true;
});
</script>
```

### Action Buttons (Icon Only)
```html
<a href="#" class="btn btn-action btn-action-primary">
    <i class="fas fa-eye"></i>
</a>

<a href="#" class="btn btn-action btn-action-danger">
    <i class="fas fa-trash"></i>
</a>
```

---

## Cards

### Standard Card
```html
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">Card Title</h5>
    </div>
    <div class="card-body">
        <!-- Content -->
    </div>
</div>
```

### Statistics Card
```html
<a href="{{ url_for('subscribers') }}" class="text-decoration-none">
    <div class="card card-stat">
        <div class="card-body text-center">
            <i class="fas fa-users"></i>
            <h5>125</h5>
            <p class="mb-0">Total Subscribers</p>
        </div>
    </div>
</a>
```

### Card with Hover Effect
```css
.card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

---

## Forms

### Text Input
```html
<div class="mb-3">
    <label for="email" class="form-label">Email Address *</label>
    <input type="email" class="form-control" id="email" name="email" 
           required aria-describedby="emailHelp">
    <div id="emailHelp" class="form-text">Enter a valid email address</div>
    <div class="invalid-feedback">Please provide a valid email</div>
</div>
```

### Input with Icon
```html
<div class="input-group">
    <span class="input-group-text">
        <i class="fas fa-search"></i>
    </span>
    <input type="text" class="form-control" placeholder="Search...">
</div>
```

### Select Dropdown
```html
<div class="mb-3">
    <label for="template" class="form-label">Select Template</label>
    <select class="form-select" id="template" name="template">
        <option value="">Choose...</option>
        <option value="1">Template 1</option>
    </select>
</div>
```

### Textarea
```html
<div class="mb-3">
    <label for="content" class="form-label">Content</label>
    <textarea class="form-control" id="content" rows="5"></textarea>
</div>
```

### Form Validation
```javascript
const input = document.getElementById('email');

input.addEventListener('blur', function() {
    if (this.validity.valid) {
        this.classList.remove('is-invalid');
        this.classList.add('is-valid');
    } else {
        this.classList.remove('is-valid');
        this.classList.add('is-invalid');
    }
});
```

---

## Empty States

### Basic Empty State
```html
<div class="empty-state text-center">
    <div class="empty-state-icon mb-4">
        <i class="fas fa-users fa-4x"></i>
    </div>
    <h4 class="text-muted mb-3">No items found</h4>
    <p class="text-muted mb-4">Get started by creating your first item.</p>
    <a href="#" class="btn btn-primary btn-lg">
        <i class="fas fa-plus me-2"></i> Create Item
    </a>
</div>
```

### Empty State with Multiple Actions
```html
<div class="empty-state text-center">
    <div class="empty-state-icon mb-4">
        <i class="fas fa-paper-plane fa-4x"></i>
    </div>
    <h4 class="text-muted mb-3">No campaigns yet</h4>
    <p class="text-muted mb-4">Create your first campaign to start!</p>
    <div class="d-flex gap-2 justify-content-center flex-wrap">
        <a href="#" class="btn btn-primary btn-lg">Create Campaign</a>
        <a href="#" class="btn btn-outline-primary btn-lg">Learn More</a>
    </div>
</div>
```

---

## Badges & Status Indicators

### Status Badges
```html
<!-- Success -->
<span class="badge bg-success status-badge">
    <i class="fas fa-check-circle"></i> Active
</span>

<!-- Warning -->
<span class="badge bg-warning status-badge">
    <i class="fas fa-clock"></i> Pending
</span>

<!-- Danger -->
<span class="badge bg-danger status-badge">
    <i class="fas fa-times-circle"></i> Failed
</span>

<!-- Secondary -->
<span class="badge bg-secondary status-badge">
    <i class="fas fa-ban"></i> Inactive
</span>
```

---

## Tables

### Responsive Table
```html
<div class="table-responsive">
    <table class="table table-hover">
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>John Doe</td>
                <td>john@example.com</td>
                <td><span class="badge bg-success">Active</span></td>
                <td>
                    <a href="#" class="btn btn-action btn-action-primary">
                        <i class="fas fa-eye"></i>
                    </a>
                    <a href="#" class="btn btn-action btn-action-danger">
                        <i class="fas fa-trash"></i>
                    </a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

---

## Pagination

```html
<nav aria-label="Page navigation" class="mt-4">
    <ul class="pagination justify-content-center">
        <li class="page-item">
            <a class="page-link" href="?page=1">Previous</a>
        </li>
        <li class="page-item active">
            <span class="page-link">1</span>
        </li>
        <li class="page-item">
            <a class="page-link" href="?page=2">2</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="?page=3">3</a>
        </li>
        <li class="page-item">
            <a class="page-link" href="?page=2">Next</a>
        </li>
    </ul>
</nav>
```

---

## Alerts & Messages

### Flash Messages
```html
<div class="alert alert-success alert-dismissible fade show" role="alert">
    <i class="fas fa-check-circle me-2"></i>
    {{ message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### Toast Notification
```javascript
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        </div>
        <div class="toast-message">${message}</div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

// Usage
showToast('Item saved successfully!', 'success');
showToast('An error occurred', 'error');
```

---

## Animations

### Hover Effect
```css
.card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Slide-In Animation
```css
@keyframes slideIn {
    from {
        transform: translateX(400px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.slide-in {
    animation: slideIn 0.3s ease;
}
```

### Loading Spinner
```css
@keyframes spinner {
    to { transform: rotate(360deg); }
}

.btn-loading::after {
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid currentColor;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spinner 0.6s linear infinite;
}
```

### Fade In/Out
```css
.fade-in {
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

---

## Icons

### Font Awesome Icons
```html
<!-- Common Icons -->
<i class="fas fa-users"></i>          <!-- Users -->
<i class="fas fa-envelope"></i>       <!-- Email -->
<i class="fas fa-paper-plane"></i>    <!-- Send -->
<i class="fas fa-plus"></i>           <!-- Add -->
<i class="fas fa-edit"></i>           <!-- Edit -->
<i class="fas fa-trash"></i>          <!-- Delete -->
<i class="fas fa-search"></i>         <!-- Search -->
<i class="fas fa-check"></i>          <!-- Success -->
<i class="fas fa-times"></i>          <!-- Close -->
<i class="fas fa-arrow-left"></i>     <!-- Back -->
<i class="fas fa-download"></i>       <!-- Download -->
<i class="fas fa-upload"></i>         <!-- Upload -->
<i class="fas fa-cog"></i>            <!-- Settings -->
<i class="fas fa-chart-line"></i>     <!-- Analytics -->
<i class="fas fa-spinner fa-spin"></i><!-- Loading -->
```

### Icon with Text
```html
<button class="btn btn-primary">
    <i class="fas fa-save me-2"></i> Save
</button>
```

---

## Responsive Utilities

### Display Classes
```html
<!-- Hide on mobile -->
<div class="d-none d-md-block">Desktop only</div>

<!-- Show only on mobile -->
<div class="d-block d-md-none">Mobile only</div>

<!-- Responsive flex -->
<div class="d-flex flex-column flex-md-row">
    <!-- Stacks on mobile, row on desktop -->
</div>
```

### Breakpoints
```css
/* Mobile First */
@media (min-width: 576px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 992px) { /* lg */ }
@media (min-width: 1200px) { /* xl */ }

/* Desktop First */
@media (max-width: 767px) { /* Mobile */ }
@media (max-width: 991px) { /* Tablet */ }
```

---

## Accessibility

### Skip Link
```html
<a href="#main-content" class="visually-hidden-focusable">
    Skip to main content
</a>
```

### ARIA Labels
```html
<!-- Button -->
<button aria-label="Close dialog">
    <i class="fas fa-times"></i>
</button>

<!-- Input -->
<input type="search" aria-label="Search subscribers">

<!-- Nav -->
<button aria-expanded="false" aria-label="Toggle navigation">
    Menu
</button>
```

### Form Accessibility
```html
<label for="email">Email</label>
<input type="email" id="email" 
       aria-describedby="emailHelp" 
       aria-required="true">
<div id="emailHelp">Help text</div>
```

---

## Common Patterns

### Page Header
```html
<div class="d-flex justify-content-between flex-wrap flex-md-nowrap 
            align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">Page Title</h1>
    <div class="btn-toolbar mb-2 mb-md-0">
        <a href="#" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New
        </a>
    </div>
</div>
```

### Search Bar
```html
<div class="card mb-3">
    <div class="card-body">
        <form class="d-flex gap-2">
            <div class="input-group flex-grow-1">
                <span class="input-group-text">
                    <i class="fas fa-search"></i>
                </span>
                <input type="text" class="form-control" placeholder="Search...">
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
</div>
```

### Confirmation Dialog
```javascript
function confirmDelete(name) {
    return confirm(`Are you sure you want to delete "${name}"? This action cannot be undone.`);
}

// Usage
<a href="/delete/1" onclick="return confirmDelete('Item Name')">Delete</a>
```

---

## Best Practices

### ✅ Do
- Use CSS variables for colors
- Add loading states for async operations
- Include ARIA labels for accessibility
- Test on mobile devices
- Use semantic HTML
- Add hover effects for interactive elements
- Provide clear error messages
- Use consistent spacing

### ❌ Don't
- Hard-code colors in CSS
- Leave buttons without disabled states
- Forget mobile responsiveness
- Use generic error messages
- Mix different animation speeds
- Ignore keyboard navigation
- Use tiny touch targets on mobile
- Create inconsistent spacing

---

## Quick Checklist

Before committing UI changes, check:

- [ ] Responsive on mobile (< 768px)
- [ ] Keyboard accessible (Tab navigation)
- [ ] Loading states for async actions
- [ ] Error states for forms
- [ ] ARIA labels for screen readers
- [ ] Consistent color usage (CSS variables)
- [ ] Hover effects on interactive elements
- [ ] Focus indicators visible
- [ ] Empty states designed
- [ ] Animations smooth (60fps)

---

**Quick Reference Version**: 1.0  
**Last Updated**: October 18, 2025  
**For**: Newsletter Application UI Development
