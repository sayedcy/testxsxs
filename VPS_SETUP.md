# VPS Setup Guide

## Configuration for VPS IP: 37.60.241.19

### Step 1: Update Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
cd frontend
echo VITE_API_URL=http://37.60.241.19:8000 > .env
```

Or manually create `frontend/.env` with:
```
VITE_API_URL=http://37.60.241.19:8000
```

### Step 2: Update Backend CORS (Already Done)

The backend CORS has been updated to allow your VPS IP. If you need to add more origins, edit `backend/main.py`.

### Step 3: Start Backend on VPS

```bash
cd backend
python main.py
```

Or with uvicorn directly:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend will be accessible at: `http://37.60.241.19:8000`

### Step 4: Start Frontend on VPS

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

The frontend will be accessible at: `http://37.60.241.19:5173`

### Step 5: Firewall Configuration

Make sure these ports are open in your firewall:

```bash
# Ubuntu/Debian
sudo ufw allow 8000/tcp
sudo ufw allow 5173/tcp
sudo ufw reload

# Or if using iptables
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5173 -j ACCEPT
```

### Step 6: Using Nginx (Recommended for Production)

Create `/etc/nginx/sites-available/security-scanner`:

```nginx
server {
    listen 80;
    server_name 37.60.241.19;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/security-scanner /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Then update `frontend/.env`:
```
VITE_API_URL=http://37.60.241.19
```

And update `frontend/src/config.js` to use relative URLs or the domain.

### Step 7: Run as Systemd Services (Optional)

Create `/etc/systemd/system/security-scanner-backend.service`:

```ini
[Unit]
Description=Security Scanner Backend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/mano/backend
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/security-scanner-frontend.service`:

```ini
[Unit]
Description=Security Scanner Frontend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/mano/frontend
ExecStart=/usr/bin/npm run dev -- --host 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable security-scanner-backend
sudo systemctl enable security-scanner-frontend
sudo systemctl start security-scanner-backend
sudo systemctl start security-scanner-frontend
```

### Troubleshooting

1. **Frontend can't connect to backend:**
   - Check if backend is running: `curl http://37.60.241.19:8000/docs`
   - Check firewall rules
   - Verify API_BASE_URL in frontend config

2. **CORS errors:**
   - Make sure VPS IP is in CORS allow_origins in `backend/main.py`
   - Check browser console for specific error

3. **Port already in use:**
   - Check what's using the port: `sudo lsof -i :8000` or `sudo netstat -tulpn | grep 8000`
   - Kill the process or change the port

4. **Build frontend for production:**
   ```bash
   cd frontend
   npm run build
   # Serve the dist folder with nginx or a static server
   ```

