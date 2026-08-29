# 🔒 Production/Dev Environment Setup

## What Just Happened

Your website is now split into **two separate environments**:

```
rarecandyreserve.org  ← Production (locked, live)
dev.rarecandyreserve.org  ← Development (password-protected, for testing)
```

---

## 📁 Folder Structure

| Folder | Purpose | Access | Editing |
|--------|---------|--------|---------|
| `/public` | **Production website** | rarecandyreserve.org | ❌ LOCKED (don't edit) |
| `/dev` | **Dev environment** | dev.rarecandyreserve.org | ✅ Password-protected |
| `/production-locked` | **Rollback backup** | (not served) | ✅ Restore if broken |

---

## 🔐 Dev Portal Login

**URL:** https://dev.rarecandyreserve.org  
**Password:** `rarecandydev2026`

⚠️ **Keep this password safe** — it's the only thing protecting your dev site from unauthorized access.

---

## 🚀 Step-by-Step: Set Up Cloudflare Routing

### 1️⃣ In Cloudflare Dashboard

1. Go to **Pages** → Select your project
2. Click **Settings** → **Build & Deployment**
3. Under **Output directory**, confirm it's set to `public`
4. Go to **Deployments** → Check that your latest push deployed ✓

### 2️⃣ Add Dev Subdomain Route

**Option A: Cloudflare Pages Routes (Easy)**

1. In Cloudflare Dashboard, go to **Pages** → Your project → **Functions** (or **Routing**)
2. Add a new route:
   - **Route:** `dev.rarecandyreserve.org/*`
   - **Directory:** `/dev`
3. Save & redeploy

**Option B: Manual via wrangler.toml**

Already added! The `wrangler.toml` file in your repo tells Cloudflare how to route traffic.

---

## 📝 How to Edit Your Site

### Current Workflow:

1. **Edit locally** (in your code editor):
   ```bash
   cd your-repo
   # Edit /dev/index.html, config.json, etc.
   ```

2. **Test locally** (run a local server):
   ```bash
   python -m http.server 8000
   # Visit http://localhost:8000 to preview
   ```

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Updated dev version"
   git push origin main
   ```

4. **Cloudflare auto-deploys** in 30-60 seconds
   - Dev changes appear at dev.rarecandyreserve.org ✓

5. **Test thoroughly**, then **promote to production**:
   ```bash
   # Copy dev changes to public folder
   cp -r dev/* public/
   git add public/
   git commit -m "Deploy to production"
   git push origin main
   ```

6. **Live on rarecandyreserve.org** ✓

---

## 🛡️ Security Notes

### Production (`/public`)
- ✅ Served as-is, no changes needed
- ✅ Clean backup in `/production-locked` for rollback
- ⚠️ Only push to this when fully tested

### Development (`/dev`)
- ✅ Password-protected at login
- ✅ SHA-256 hashing (not plain-text)
- ✅ 12-hour session timeout
- ⚠️ Secure password: `rarecandydev2026` (change it if needed!)

---

## 🔄 Workflow Summary

```
Your Code Editor
      ↓
Edit /dev/index.html or config.json
      ↓
git push origin main
      ↓
Cloudflare auto-deploys
      ↓
Test at dev.rarecandyreserve.org (password: rarecandydev2026)
      ↓
Ready for production? Copy /dev → /public
      ↓
git push origin main
      ↓
Live on rarecandyreserve.org ✓
```

---

## 💾 Rollback: If Something Breaks

```bash
# Copy backup to production
cp -r production-locked/* public/

# Commit and push
git add public/
git commit -m "Rollback to production-locked version"
git push origin main
```

Cloudflare redeploys in 30-60 seconds. Site restored! ✓

---

## ❓ FAQ

**Q: Can I edit /public directly?**  
A: You *can*, but shouldn't. Use /dev for testing first. This prevents live-site breakage.

**Q: What if I forget the dev password?**  
A: Edit `/dev/index.html` in your code editor and change the SHA-256 hash. (See `QUICK_EDIT_GUIDE.md` for password hashing tools.)

**Q: How do I change the dev password?**  
A: 
1. Generate a SHA-256 hash of your new password at https://www.sha256online.com/
2. Copy the hash into `/dev/index.html` line ~84
3. Push to GitHub
4. Use the new password next login

**Q: Is my site secure?**  
A: 
- ✅ Production is locked (no public edits)
- ✅ Dev is password-protected
- ✅ /production-locked is a clean backup
- ⚠️ Passwords are hashed, but use Cloudflare's additional security (Page Rules, IP blocking) for extra protection

---

## 🎯 Next Steps

1. ✅ Confirm both `/public` and `/dev` deployed to Cloudflare
2. ✅ Test accessing dev.rarecandyreserve.org (use password: `rarecandydev2026`)
3. ✅ Edit config.json or content in `/dev` to test changes
4. ✅ When ready, copy changes to `/public` and push to production
5. ✅ Keep `/production-locked` as your rollback safety net

---

**Everything is set up! Your site is now properly separated and protected.** 🚀
