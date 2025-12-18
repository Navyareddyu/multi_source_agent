# Connect Your Git Repository

## Quick Setup Steps

### 1. Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `multi_source_agent` (or your choice)
3. **Don't** check "Initialize with README"
4. Click "Create repository"

### 2. Connect Local Repository to GitHub

After creating the repo, GitHub will show you commands. Use these:

```bash
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. Example (if your username is "tejareddy" and repo is "multi_source_agent"):

```bash
git remote add origin https://github.com/tejareddy/multi_source_agent.git
git branch -M main
git push -u origin main
```

## What's Already Done ✅

- ✅ Git initialized
- ✅ `.gitignore` created (excludes databases, cache, etc.)
- ✅ Initial commit created
- ✅ All files staged and committed

## Verify Connection

After running the commands above, verify:

```bash
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (fetch)
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (push)
```

## Next Steps After Connecting

Once connected, you can:
1. **Deploy to Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub repo
2. **Share your code**: Others can clone and contribute
3. **Track changes**: All future commits will sync to GitHub

## Troubleshooting

**If you get "remote origin already exists":**
```bash
git remote remove origin
# Then add it again with the correct URL
```

**If you get authentication errors:**
- Use a Personal Access Token instead of password
- Or set up SSH keys: [GitHub SSH Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

