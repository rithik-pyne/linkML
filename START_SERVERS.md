# How to Start the Dashboard

## Quick Start

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open: **http://localhost:5173**

---

## Troubleshooting

### Images Not Showing?

1. **Check backend is serving static files:**
   ```bash
   curl -I http://localhost:8000/static/imaging/thumbnails/lung_ct_001_thumb.jpg
   ```
   Should return: `HTTP/1.1 200 OK`

2. **Check files exist:**
   ```bash
   ls backend/static/imaging/thumbnails/
   ```
   Should show 7 `.jpg` files

3. **Restart backend** (after code changes):
   - Press `Ctrl+C` in backend terminal
   - Run uvicorn command again

### API Not Working?

Test the API:
```bash
curl http://localhost:8000/api/patients/NGDX-001/imaging
```

Should return JSON with imaging_studies array.

### Frontend Not Loading?

1. Check Vite is running on port 5173
2. Check browser console for errors (F12)
3. Try: `cd frontend && npm install` then `npm run dev`

---

## Testing the Imaging Tab

1. Select patient: **NGDX-001**
2. Click **"Imaging Studies"** tab
3. Should see grid of 5 study cards with thumbnails
4. Click **"View Full Image"** on any card
5. Modal should open with full CT image

---

## Quick Verification

Run this to verify everything is ready:

```bash
# Check database
python -c "import sqlite3; conn = sqlite3.connect('backend/clinical_data.db'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM ImagingStudy WHERE dicom_file_path IS NOT NULL'); print(f'{c.fetchone()[0]} studies have images')"

# Check image files
ls backend/static/imaging/full/ | wc -l
# Should output: 7

# Check thumbnails
ls backend/static/imaging/thumbnails/ | wc -l
# Should output: 7
```

Expected output:
```
25 studies have images
7
7
```

All ready! ✓