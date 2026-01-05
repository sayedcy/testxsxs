# Registration Fix - Troubleshooting Guide

## Changes Made

1. **Added username uniqueness check** - Now checks both email and username before registration
2. **Improved error handling** - Better error messages for users
3. **Added try-catch blocks** - Prevents crashes on database errors

## Common Issues and Solutions

### Issue 1: "Registration failed" with no specific error

**Check:**
1. Open browser console (F12) and look for errors
2. Check if backend is running: `http://37.60.241.19:8000/docs`
3. Verify API URL in `frontend/src/config.js` matches your backend URL

**Solution:**
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify API_BASE_URL in frontend config

### Issue 2: "Email already registered"

**Solution:**
- Use a different email address
- Or delete the existing user from database

### Issue 3: "Username already taken"

**Solution:**
- Choose a different username
- The system now checks username uniqueness

### Issue 4: CORS Errors

**Check browser console for:**
```
Access to XMLHttpRequest at 'http://...' from origin 'http://...' has been blocked by CORS policy
```

**Solution:**
- Make sure your frontend URL is in the CORS allow_origins list in `backend/main.py`
- The backend should have `"*"` for development, but verify it includes your VPS IP

### Issue 5: Network Errors

**Check:**
- Is the backend running? Test: `curl http://37.60.241.19:8000/docs`
- Is the API URL correct in `frontend/src/config.js`?

**Solution:**
- Verify backend is accessible
- Check firewall rules
- Test API directly: `curl -X POST http://37.60.241.19:8000/api/register -H "Content-Type: application/json" -d '{"email":"test@test.com","username":"test","password":"test123"}'`

## Testing Registration

### Test Backend Directly:

```bash
curl -X POST http://37.60.241.19:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "test123456"
  }'
```

### Check Database:

```bash
# If using SQLite
sqlite3 backend/scanner.db
SELECT * FROM users;
```

## Debug Steps

1. **Check Backend Logs:**
   - Look at the terminal where backend is running
   - Check for any error messages

2. **Check Frontend Console:**
   - Open browser DevTools (F12)
   - Go to Console tab
   - Look for red error messages
   - Go to Network tab to see API requests

3. **Verify API Endpoint:**
   - Visit: `http://37.60.241.19:8000/docs`
   - Try the `/api/register` endpoint manually
   - Check if it returns errors

4. **Check API Configuration:**
   - Verify `frontend/src/config.js` has correct API URL
   - Or check `frontend/.env` file has `VITE_API_URL=http://37.60.241.19:8000`

## Quick Fix Checklist

- [ ] Backend is running on port 8000
- [ ] Frontend is running and can access backend
- [ ] API URL in config.js matches backend URL
- [ ] CORS is configured correctly
- [ ] Database file exists and is writable
- [ ] No console errors in browser
- [ ] Network tab shows API request is being made

