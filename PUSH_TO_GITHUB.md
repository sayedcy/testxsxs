# How to Push to GitHub - Step by Step Guide

## Step 1: Install Git (if not installed)

1. Download Git for Windows: https://git-scm.com/download/win
2. Run the installer and use default settings
3. **Restart your terminal/PowerShell** after installation

## Step 2: Verify Git Installation

Open PowerShell and run:
```powershell
git --version
```

You should see something like: `git version 2.x.x`

## Step 3: Configure Git (First Time Only)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 4: Navigate to Your Project

```powershell
cd C:\Users\memos\Desktop\mano
```

## Step 5: Initialize Git Repository (if not already done)

```powershell
git init
```

## Step 6: Add All Files

```powershell
git add .
```

## Step 7: Create Initial Commit

```powershell
git commit -m "Initial commit: Security Scanner with VPS support"
```

## Step 8: Create GitHub Repository

1. Go to https://github.com and sign in
2. Click the **+** icon (top right) → **New repository**
3. Name it (e.g., `security-scanner` or `mano`)
4. **DO NOT** check "Initialize with README" (we already have files)
5. Click **Create repository**

## Step 9: Connect and Push to GitHub

After creating the repository, GitHub will show you commands. Use these (replace `YOUR_USERNAME` and `YOUR_REPO_NAME`):

```powershell
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note:** When prompted for credentials:
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (not your GitHub password)

### How to Create Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name it (e.g., "My Computer")
4. Select scope: **repo** (check all repo permissions)
5. Click **Generate token**
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing

## Step 10: Future Updates

When you make changes and want to push updates:

```powershell
# Check what changed
git status

# Add all changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Complete Command Sequence (Copy & Paste)

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values:

```powershell
cd C:\Users\memos\Desktop\mano
git init
git add .
git commit -m "Initial commit: Security Scanner with VPS support"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Troubleshooting

### "git is not recognized"
- Git is not installed or not in PATH
- Restart terminal after installing Git
- Or use Git Bash instead of PowerShell

### "Authentication failed"
- GitHub requires Personal Access Token, not password
- Create token at: https://github.com/settings/tokens
- Use token as password

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### "fatal: not a git repository"
```powershell
git init
```

### "Everything up-to-date"
- No changes to push
- Make sure you've committed: `git commit -m "message"`

## Alternative: Using GitHub Desktop

If you prefer a GUI:
1. Download: https://desktop.github.com/
2. Sign in with GitHub
3. File → Add Local Repository
4. Select your folder: `C:\Users\memos\Desktop\mano`
5. Click "Publish repository"

