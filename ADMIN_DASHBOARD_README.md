# 🛡️ Admin Dashboard - Documentation

## Overview

The Admin Dashboard is a powerful web-based interface for managing your Faner Studio platform. It provides comprehensive monitoring, user management, and system analytics.

---

## 🌟 Features

### 📊 Dashboard Statistics
- **Total Users**: Track registered users
- **Total Projects**: Monitor all projects (audiobooks, podcasts)
- **Custom Voices**: View voice library statistics
- **System Health**: Real-time system monitoring

### 👥 User Management
- View all registered users
- Edit user status (active/inactive)
- Promote users to admin role
- Delete user accounts
- View user creation dates and activity

### 📁 Project Management
- View all projects across all users
- Monitor project status (pending, processing, completed, failed)
- Track project progress
- Delete projects
- Filter by project type

### 🎤 Voice Management
- View all custom voices
- Track voice usage statistics
- Monitor voice ratings
- Manage public/private voices

### 🖥️ System Monitoring
- Real-time CPU usage
- Memory usage tracking
- Disk space monitoring
- Cache status
- Database connection status

---

## 🔐 Access

### URL
```
Local:      http://localhost:8000/admin
Production: https://fanerstudio-1.onrender.com/admin
```

### Default Admin Credentials
```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT**: Change default credentials in production!

---

## 📡 API Endpoints

### Authentication
```
POST /api/auth/login
  - Login and get JWT token

GET /api/auth/me
  - Get current user info
```

### Admin Stats
```
GET /api/admin/stats
  - Get dashboard statistics
  - Requires: Admin role
  - Returns: Total counts and weekly changes
```

### User Management
```
GET /api/admin/users?limit=100&offset=0
  - Get all users
  - Requires: Admin role

PUT /api/admin/user/{user_id}
  - Update user status/role
  - Requires: Admin role
  - Body: { is_active: bool, is_admin: bool }

DELETE /api/admin/user/{user_id}
  - Delete user
  - Requires: Admin role
```

### Project Management
```
GET /api/admin/projects?limit=100&offset=0
  - Get all projects
  - Requires: Admin role

DELETE /api/admin/project/{project_id}
  - Delete project
  - Requires: Admin role
```

### Voice Management
```
GET /api/admin/voices?limit=100&offset=0
  - Get all custom voices
  - Requires: Admin role
```

### System Monitoring
```
GET /api/performance/system
  - Get system stats (CPU, RAM, Disk)
  - Public endpoint

GET /api/performance/stats
  - Get API performance stats
  - Public endpoint

GET /api/performance/cache
  - Get cache information
  - Public endpoint
```

---

## 🛠️ Setup & Testing

### 1. Create Admin User

First, create an admin user in your database:

```python
# Run test_database.py or manually create admin user
from database import SessionLocal, UserCRUD
from auth import hash_password

db = SessionLocal()

admin_user = UserCRUD.create_user(
    db=db,
    username="admin",
    email="admin@fanerstudio.com",
    hashed_password=hash_password("admin123"),
    full_name="System Administrator"
)

# Set admin flag
admin_user.is_admin = True
db.commit()
```

### 2. Test Locally

```bash
# Run the test script
python test_admin_dashboard.py

# Or use batch file
TEST_ADMIN_DASHBOARD.bat
```

### 3. Access Dashboard

Open browser:
```
http://localhost:8000/admin
```

Login with admin credentials.

---

## 📊 Dashboard Sections

### 1. Statistics Cards
Shows key metrics at a glance:
- Total users (with weekly growth)
- Total projects (with weekly growth)
- Custom voices (with weekly growth)
- System health (100% = all services operational)

### 2. Users Table
Displays all registered users with:
- ID, Username, Email, Full Name
- Status badge (Active/Inactive)
- Role badge (Admin/User)
- Creation date
- Action buttons (Edit, Delete)

### 3. Projects Table
Shows all projects with:
- ID, Type, Title, User
- Status badge (Pending, Processing, Completed, Failed)
- Progress percentage
- Creation date
- Action buttons (View, Delete)

### 4. System Monitoring
Real-time system metrics:
- CPU usage (progress bar + percentage)
- Memory usage (progress bar + percentage)
- Disk usage (progress bar + percentage)
- Cache status (Enabled/Disabled)
- Database status (Enabled/Disabled)

### 5. Activity Log
*(Coming soon)*
- User actions
- API calls
- System events
- Error logs

---

## 🔒 Security

### Authentication
- JWT-based authentication
- Token stored in localStorage
- Automatic token validation
- Admin role verification

### Authorization
All admin endpoints check:
1. Valid JWT token
2. User is authenticated
3. User has `is_admin = True`

### Best Practices
1. **Change default password** immediately
2. **Use HTTPS** in production
3. **Rotate JWT secret** regularly
4. **Monitor admin actions** via activity logs
5. **Limit admin accounts** to trusted users only

---

## 🎨 Customization

### Color Scheme
Edit CSS variables in `admin_dashboard.html`:
```css
:root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --accent-blue: #3b82f6;
    /* ... more colors */
}
```

### API Base URL
Change in JavaScript section:
```javascript
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://fanerstudio-1.onrender.com';
```

### Auto-refresh Interval
Modify in JavaScript:
```javascript
// Current: 30 seconds
setInterval(() => {
    loadStats();
    loadSystemStats();
}, 30000);  // Change to desired milliseconds
```

---

## 🐛 Troubleshooting

### Issue: "Admin privileges required"
**Solution**: Verify user has `is_admin = True` in database

### Issue: "Database not available"
**Solution**: 
- Check `DATABASE_URL` environment variable
- Verify Supabase connection
- Run database initialization

### Issue: Stats show "--"
**Solution**:
- Check API endpoint is accessible
- Verify JWT token is valid
- Check browser console for errors

### Issue: "Failed to load users/projects"
**Solution**:
- Verify database has data
- Check API endpoint returns 200
- Inspect network tab in browser DevTools

---

## 📈 Future Enhancements

### Planned Features
- [ ] Activity log implementation
- [ ] Advanced user search and filters
- [ ] Project bulk actions
- [ ] Export data to CSV/JSON
- [ ] Real-time notifications
- [ ] User analytics charts (Chart.js)
- [ ] System alerts and warnings
- [ ] Backup and restore functionality
- [ ] Email notifications
- [ ] Two-factor authentication

---

## 🚀 Deployment

### Deploy to Render

1. **Commit changes:**
```bash
git add admin_dashboard.html main.py test_admin_dashboard.py
git commit -m "Add admin dashboard"
git push origin master
```

2. **Render auto-deploys** via GitHub Actions

3. **Access dashboard:**
```
https://fanerstudio-1.onrender.com/admin
```

4. **Verify admin user exists** in Supabase

---

## 📞 Support

For issues or questions:
- Check `/docs` endpoint for API documentation
- Review browser console for JavaScript errors
- Inspect network tab for failed API calls
- Check Render logs for backend errors

---

## ✅ Checklist

Before going to production:

- [ ] Create admin user account
- [ ] Change default admin password
- [ ] Set secure `SECRET_KEY` environment variable
- [ ] Enable HTTPS
- [ ] Test all admin endpoints
- [ ] Verify role-based access control
- [ ] Monitor system resources
- [ ] Set up activity logging
- [ ] Configure auto-backups
- [ ] Document admin procedures

---

**Admin Dashboard Version**: 1.0.0  
**Last Updated**: November 2024  
**Platform**: Faner Studio Complete

