# Push Your Code to GitHub

## Authentication Required

GitHub requires authentication to push code. Choose one method below:

## Option 1: Personal Access Token (Recommended for HTTPS)

### Step 1: Create a Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: "multi_source_agent"
4. Select scopes: Check `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

### Step 2: Push using the token
```bash
git push -u origin main
```
When prompted:
- **Username**: `Navyareddyu`
- **Password**: Paste your personal access token (NOT your GitHub password)

---

## Option 2: Use SSH (More Secure, One-Time Setup)

### Step 1: Check if you have SSH keys
```bash
ls -la ~/.ssh
```

### Step 2: Generate SSH key (if needed)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default file location
# Optionally set a passphrase
```

### Step 3: Add SSH key to GitHub
```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
# Copy the output
```

Then:
1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Paste your public key
4. Save

### Step 4: Change remote URL to SSH
```bash
git remote set-url origin git@github.com:Navyareddyu/multi_source_agent.git
git push -u origin main
```

---

## Option 3: Use GitHub CLI (If installed)

```bash
gh auth login
git push -u origin main
```

---

## After Successful Push

Your code will be available at:
**https://github.com/Navyareddyu/multi_source_agent**

## Next Steps

Once pushed, you can:
1. **Deploy to Streamlit Cloud**: https://share.streamlit.io
2. **Share your repository** with others
3. **Continue development** and push future changes

## Troubleshooting

**Error: "Updates were rejected"**
- The remote has commits you don't have locally
- Run: `git pull origin main --allow-unrelated-histories`
- Then: `git push -u origin main`

**Error: "Permission denied"**
- Check your token/SSH key has `repo` permissions
- Verify you're using the correct username

