# How to Add a New GitHub Repository

## Step 1: Create Repository on GitHub

1. Go to https://github.com and sign in
2. Click the **+** icon (top right corner) → **New repository**
3. Fill in the details:
   - **Repository name:** (e.g., `security-scanner`, `mano-scanner`)
   - **Description:** (optional) "Security vulnerability scanning web application"
   - **Visibility:** Choose Public or Private
   - **DO NOT** check "Add a README file" (we already have files)
   - **DO NOT** check "Add .gitignore" (we already have one)
   - **DO NOT** choose a license (unless you want to add one)
4. Click **Create repository**

## Step 2: After Installing Git, Run These Commands

Open PowerShell in your project folder and run:

### Option A: If you DON'T have a remote yet (First time)

```powershell
# Navigate to project
cd C:\Users\memos\Desktop\mano

# Add the new remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Check it was added
git remote -v

# Add all files
git add .

# Commit
git commit -m "Initial commit: Security Scanner Application"

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: If you ALREADY have a remote (Replace existing)

```powershell
# Remove old remote
git remote remove origin

# Add new remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Verify new remote
git remote -v

# Push to new repository
git push -u origin main
```

### Option C: Add Multiple Remotes (Keep old + add new)

```powershell
# Add new remote with a different name (e.g., "newrepo")
git remote add newrepo https://github.com/YOUR_USERNAME/NEW_REPO_NAME.git

# Push to new repository
git push -u newrepo main

# To push to both:
git push origin main    # Old repository
git push newrepo main  # New repository
```

## Step 3: Authentication

When you push, GitHub will ask for credentials:
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (NOT your GitHub password)

### Create Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name: "My Computer" or "Windows PC"
4. Expiration: Choose duration (90 days recommended)
5. Select scopes: Check **repo** (all repository permissions)
6. Click **Generate token**
7. **COPY THE TOKEN** (you won't see it again!)
8. Use this token as your password when pushing

## Complete Example

Replace these values:
- `YOUR_USERNAME` = Your GitHub username (e.g., `johndoe`)
- `REPO_NAME` = Your repository name (e.g., `security-scanner`)

```powershell
cd C:\Users\memos\Desktop\mano
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git add .
git commit -m "Initial commit: Security Scanner with VPS support"
git branch -M main
git push -u origin main
```

## Verify It Worked

After pushing, you should see:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/YOUR_USERNAME/REPO_NAME.git
 * [new branch]      main -> main
```

Then visit: `https://github.com/YOUR_USERNAME/REPO_NAME` to see your code!

## Troubleshooting

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### "fatal: not a git repository"
```powershell
git init
```

### "git is not recognized"
- Install Git: https://git-scm.com/download/win
- Restart PowerShell after installation

### "Authentication failed"
- Make sure you're using Personal Access Token, not password
- Create new token at: https://github.com/settings/tokens

### "Repository not found"
- Check repository name spelling
- Make sure repository exists on GitHub
- Verify you have access to the repository

## Quick Reference

```powershell
# Check current remotes
git remote -v

# Add new remote
git remote add origin https://github.com/USERNAME/REPO.git

# Remove remote
git remote remove origin

# Change remote URL
git remote set-url origin https://github.com/USERNAME/NEW_REPO.git

# Push to remote
git push -u origin main
```

