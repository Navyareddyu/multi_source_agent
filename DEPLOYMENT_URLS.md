# Deployment URLs

## Current Deployments

### Production URL
**https://multisourceagent-master.vercel.app**

### Preview/Other Deployment
**https://multi-source-agent-6ummsnovj-navyas-projects-7b4306f5.vercel.app**

This appears to be a different deployment (possibly from a different Vercel account or project).

## How Vercel URLs Work

Vercel creates URLs in these formats:
- **Production**: `your-project-name.vercel.app`
- **Preview**: `your-project-name-[hash]-[account].vercel.app`
- **Custom Domain**: Your domain (if configured)

## Check Your Active Deployment

1. **Vercel Dashboard**: https://vercel.com/dashboard
   - Go to your project
   - Check "Deployments" tab
   - The active deployment is marked as "Production"

2. **All URLs**:
   - Main production URL should be the same across deployments
   - Preview URLs are unique per deployment

## Testing Your App

Both URLs should work, but use the production URL for sharing:
- **Production**: https://multisourceagent-master.vercel.app
- **Test URL**: https://multi-source-agent-6ummsnovj-navyas-projects-7b4306f5.vercel.app

## Setting Up Custom Domain

If you want a custom domain:
1. Go to Vercel Dashboard → Project → Settings → Domains
2. Add your domain
3. Configure DNS records as instructed
4. The custom domain will point to your production deployment

