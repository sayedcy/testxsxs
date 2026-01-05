# How to Push to GitHub from Windows

## Step 1: Install Git (if not already installed)

1. Download Git from: https://git-scm.com/download/win
2. Install with default settings
3. Verify installation by opening PowerShell/Command Prompt and running:
   ```bash
   git --version
   ```

## Step 2: Initialize Git Repository

Open PowerShell or Command Prompt in your project folder (`C:\Users\memos\Desktop\mano`) and run:

```bash
git init
```

## Step 3: Add All Files

```bash
git add .
```

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Security Scanner Web Application"
```

## Step 5: Create GitHub Repository

1. Go to https://github.com and sign in
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Name it (e.g., `security-scanner` or `mano`)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 6: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these (replace `YOUR_USERNAME` and `YOUR_REPO_NAME`):

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Alternative: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
gh repo create YOUR_REPO_NAME --public --source=. --remote=origin --push
```

## Complete Command Sequence

Here's the full sequence in one go:

```bash
# Navigate to your project folder
cd C:\Users\memos\Desktop\mano

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Security Scanner Web Application"

# Add remote (replace with your GitHub username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Troubleshooting

### If you get authentication errors:
- GitHub no longer accepts passwords. You need to use a **Personal Access Token**:
  1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Generate new token with `repo` permissions
  3. Use the token as your password when pushing

### If you need to update later:
```bash
git add .
git commit -m "Your commit message"
git push
```

### To check status:
```bash
git status
```

### To see remote URL:
```bash
git remote -v
```

