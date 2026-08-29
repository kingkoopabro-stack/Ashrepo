# 🎨 Quick Edit Guide — Rare Candy Reserve

**Edit `public/config.json` in any text editor to update your website. No coding needed!**

---

## 📝 Easy Edits in config.json

### 🎵 **Music Player Settings**
```json
"music": {
  "spotifyArtistId": "5Yu8YngzEdVTot78vdFgnB",          // ← Your Spotify artist ID
  "spotifyArtistUrl": "https://open.spotify.com/...",  // ← Full Spotify link
  "pandoraUrl": "https://www.pandora.com/...",         // ← Pandora link
  "appleUrl": "https://music.apple.com/...",           // ← Apple Music link
  "spotifyEmbedTrackId": "5BYgK8ezleNqwQz4RiAleA",     // ← Track to embed (change this to play different song!)
  "artistName": "A Steady Heart",                      // ← Your artist name
  "themeTrack": "Enough is never enough"               // ← Homepage theme track name
}
```

✅ **To change the Spotify player track:** Only edit `spotifyEmbedTrackId` with a new track ID from Spotify.

---

### 💳 **Payment Methods**
```json
"payment": {
  "stripePublishableKey": "pk_live_YOUR_KEY_HERE",     // ← Stripe key (get from Stripe dashboard)
  "paypalClientId": "YOUR_PAYPAL_CLIENT_ID",           // ← PayPal key
  "squareLocationId": "YOUR_SQUARE_LOCATION_ID",       // ← Square key
  "defaultProvider": "stripe"                          // ← Which payment to use by default
}
```

---

### 🛍️ **Shop Categories**
```json
"categories": [
  { "name": "Authenticated Cards", "icon": "/images/b8409556-b488-456b-b63f-2fbba1039b8f-049a0d2b-37d8-4207-aa34-a57dd5098146.png" },
  // Add more categories here or edit names/image URLs
]
```

✅ **To add a category:** Copy one line, paste it, change the name and image URL.

---

### 📦 **Products for Sale**
```json
"products": [
  {
    "id": "custom-3d-print",
    "name": "Custom 3D Print",                // ← What it's called
    "price": 25.00,                          // ← Price in dollars
    "description": "Commission a custom...", // ← Short description
    "category": "Custom 3D Prints",          // ← Which category it belongs to
    "ctaText": "Request Quote",              // ← Button text (e.g., "Buy Now", "Add to Cart")
    "ctaUrl": "/submit.html"                 // ← Where button links to
  }
]
```

✅ **To add a product:** Copy a product block, paste it, fill in your details.

---

### 🏢 **Partner Links**
```json
"partners": [
  {
    "name": "7-Acre Wood Plant Nursery",
    "url": "https://7acrewoods.com"
  }
]
```

---

## 🚀 How to Deploy Changes

After editing `public/config.json`:

```bash
cd your-repo-folder
git add public/config.json
git commit -m "Updated [what you changed]"
git push origin main
```

**Cloudflare will automatically redeploy your site in 30-60 seconds!**

---

## 📖 Common Tasks

### Change Spotify Track ID
1. Go to a song on Spotify (on spotify.com)
2. Click the **three dots** → **Share** → **Copy link to song**
3. The URL looks like: `https://open.spotify.com/track/5BYgK8ezleNqwQz4RiAleA`
4. Copy just the ID part: `5BYgK8ezleNqwQz4RiAleA`
5. Paste it into `config.json` under `spotifyEmbedTrackId`

### Add a New Product
1. Copy this template:
```json
{
  "id": "my-product",
  "name": "Product Name",
  "price": 29.99,
  "description": "What is this?",
  "category": "Custom 3D Prints",
  "ctaText": "Buy Now",
  "ctaUrl": "/checkout"
}
```
2. Fill in your info
3. Paste it into the `"products"` array
4. Commit and push!

### Change Site Domain
Edit `site.domain` to match where your site is hosted:
```json
"site": {
  "domain": "https://rarecandyreserve.org"  // ← Update this
}
```

---

## ⚠️ Important Notes

- **Keep the JSON valid!** If you add commas or quotes wrong, the site breaks. Use a JSON validator: https://jsonlint.com/
- **Image URLs** must exist in `/public/images/`
- **All prices** are in USD dollars
- **Theme track** is just for display—change `spotifyEmbedTrackId` to change what actually plays

---

## 🎯 Need Help?

If something breaks:
1. Check https://jsonlint.com/ to validate config.json
2. Undo your last change
3. Try again more carefully
4. If still broken, revert with: `git checkout public/config.json`

Happy editing! 🚀
