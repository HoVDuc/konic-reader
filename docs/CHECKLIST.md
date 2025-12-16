# ✅ REFACTORING CHECKLIST

## Pre-Refactoring

- [ ] **Backup your project**
  ```bash
  cp -r albumman albumman_backup
  ```

- [ ] **Commit current state** (if using git)
  ```bash
  git add .
  git commit -m "Before refactoring"
  ```

- [ ] **Test current app works**
  ```bash
  python3 app.py  # or python3 main.py
  # Visit http://localhost:5000
  ```

- [ ] **Document current features** that work
  - [ ] Upload PDF
  - [ ] Upload ZIP
  - [ ] Upload folder
  - [ ] Create series
  - [ ] View albums
  - [ ] Other features: _______________

- [ ] **Read documentation**
  - [ ] START_HERE.md
  - [ ] REFACTORING_SUMMARY.md
  - [ ] VISUAL_GUIDE.md

## During Refactoring

- [ ] **Run refactoring script**
  ```bash
  python3 REFACTOR_NOW.py
  ```

- [ ] **Watch for errors**
  - [ ] All steps complete
  - [ ] No error messages
  - [ ] All files created

- [ ] **Verify new structure exists**
  ```bash
  ls -la app/
  ls -la config/
  ls -la data/
  ```

## Post-Refactoring Testing

### 1. Application Starts

- [ ] **Run new entry point**
  ```bash
  python3 run.py
  ```

- [ ] **No import errors**
- [ ] **No startup errors**
- [ ] **Server starts on port 5000**

### 2. Homepage

- [ ] **Visit http://localhost:5000**
- [ ] **Page loads without errors**
- [ ] **Existing albums display** (if any)
- [ ] **Existing series display** (if any)
- [ ] **Upload tabs appear**
- [ ] **Create Series button works**

### 3. Upload Features

- [ ] **Upload PDF**
  - [ ] File selection works
  - [ ] Upload starts
  - [ ] Progress bar shows
  - [ ] Conversion completes
  - [ ] Album appears in list
  
- [ ] **Upload ZIP**
  - [ ] File selection works
  - [ ] Upload starts
  - [ ] Extraction works
  - [ ] Album appears in list

- [ ] **Upload Folder**
  - [ ] Folder selection works
  - [ ] Upload completes
  - [ ] Images extracted
  - [ ] Album appears in list

### 4. Series Management

- [ ] **Create new series**
  - [ ] Input form works
  - [ ] Series created
  - [ ] Appears in list

- [ ] **Add album to series**
  - [ ] Dropdown shows series
  - [ ] Album links to series
  - [ ] Shows in series details

- [ ] **Toggle series status**
  - [ ] Mark as completed
  - [ ] Mark as ongoing
  - [ ] Badge displays correctly

- [ ] **Remove album from series**
  - [ ] Remove button works
  - [ ] Album unlinked
  - [ ] Still exists as standalone

### 5. Album Features

- [ ] **View album details**
  - [ ] Click album card
  - [ ] Details page loads
  - [ ] Image count correct
  - [ ] Cover displays

- [ ] **Read album**
  - [ ] Reader opens
  - [ ] Images load
  - [ ] Can scroll through pages
  - [ ] Images are decrypted properly

- [ ] **Navigation in reader**
  - [ ] Previous chapter works (if in series)
  - [ ] Next chapter works (if in series)
  - [ ] Back button works
  - [ ] Zoom controls work

- [ ] **Rename album**
  - [ ] Input field works
  - [ ] Name updates
  - [ ] Displays new name

- [ ] **Change cover**
  - [ ] Upload new cover
  - [ ] Cover updates
  - [ ] Delete cover works
  - [ ] Falls back to first image

- [ ] **Delete album**
  - [ ] Confirmation prompt
  - [ ] Album deleted
  - [ ] Files removed
  - [ ] Removed from lists

### 6. Series Features

- [ ] **View series details**
  - [ ] Click series card
  - [ ] Details page loads
  - [ ] Chapter list shows
  - [ ] Count correct

- [ ] **Rename series**
  - [ ] Input field works
  - [ ] Name updates

- [ ] **Change series cover**
  - [ ] Upload new cover
  - [ ] Cover updates

- [ ] **Delete series**
  - [ ] Confirmation prompt
  - [ ] Series deleted
  - [ ] Albums become standalone
  - [ ] Cover removed

### 7. API Endpoints

- [ ] **Progress tracking**
  - [ ] `/api/status/<task_id>` works
  - [ ] Returns JSON
  - [ ] Progress updates

### 8. Static Files

- [ ] **CSS loads**
  - [ ] Styles apply
  - [ ] Layout correct

- [ ] **JavaScript works**
  - [ ] Upload progress
  - [ ] Tab switching
  - [ ] Interactive elements

### 9. Data Integrity

- [ ] **Existing data accessible**
  - [ ] Old albums viewable
  - [ ] Old series intact
  - [ ] Images decrypt properly
  - [ ] Covers display

- [ ] **Database intact**
  - [ ] All records present
  - [ ] Relationships preserved

- [ ] **Files in correct locations**
  - [ ] Albums in `data/albums/`
  - [ ] Covers in `data/covers/`
  - [ ] Uploads in `data/uploads/`
  - [ ] Database in `data/instance/`

## Code Quality Checks

- [ ] **No Python syntax errors**
  ```bash
  python3 -m py_compile app/**/*.py
  ```

- [ ] **Imports work**
  ```bash
  python3 -c "from app import create_app; print('OK')"
  ```

- [ ] **Configuration loads**
  ```bash
  python3 -c "from config.development import DevelopmentConfig; print('OK')"
  ```

## Documentation Review

- [ ] **Read MIGRATION_NOTES.md**
- [ ] **Understand new structure**
- [ ] **Know where each file is**
- [ ] **Read updated README.md**

## Cleanup (After Successful Testing)

- [ ] **Remove old files**
  ```bash
  rm app.py main.py
  ```

- [ ] **Remove refactoring scripts**
  ```bash
  rm refactor_*.py execute_refactor.py extract_templates.py
  rm REFACTOR_NOW.py create_structure.py setup_structure.py
  ```

- [ ] **Remove temporary files**
  ```bash
  rm -rf __pycache__/ *.pyc *.swp
  ```

- [ ] **Clean up docs** (optional)
  ```bash
  # Keep useful ones, remove verbose guides
  rm REFACTORING_SUMMARY.md VISUAL_GUIDE.md START_HERE.md
  # Keep: REFACTORING_GUIDE.md, README.md, MIGRATION_NOTES.md
  ```

## Git Commit (if using version control)

- [ ] **Stage new files**
  ```bash
  git add app/ config/ data/ tests/ docs/
  git add run.py .env.example .gitignore README.md
  ```

- [ ] **Remove old files from git**
  ```bash
  git rm app.py main.py
  ```

- [ ] **Commit changes**
  ```bash
  git commit -m "Refactor: Restructure project for better maintainability

  - Split monolithic app.py into modules
  - Created app factory pattern
  - Extracted models, services, routes
  - Added configuration layer
  - Extracted HTML templates
  - Organized static assets
  - Updated documentation
  "
  ```

## Production Deployment (when ready)

- [ ] **Update environment**
  - [ ] Copy `.env.example` to `.env`
  - [ ] Set SECRET_KEY
  - [ ] Set DATABASE_URL (if not SQLite)

- [ ] **Install dependencies**
  ```bash
  pip install -r requirements.txt
  # or
  uv sync
  ```

- [ ] **Initialize database** (if needed)
  ```bash
  python3 -c "from app import create_app; app = create_app(); app.app_context().push(); from app import db; db.create_all()"
  ```

- [ ] **Test in production mode**
  ```bash
  FLASK_ENV=production python3 run.py
  ```

- [ ] **Set up process manager** (e.g., systemd, supervisor)

- [ ] **Configure reverse proxy** (e.g., nginx)

- [ ] **Enable HTTPS**

## Success Criteria

✅ All tests pass
✅ All features work
✅ No errors in logs
✅ Code is organized
✅ Documentation updated
✅ Team understands new structure

## If Something Goes Wrong

1. **Don't panic**
2. **Check error messages carefully**
3. **Restore from backup if needed**
   ```bash
   rm -rf albumman
   cp -r albumman_backup albumman
   ```
4. **Review logs**
5. **Re-read documentation**
6. **Try again step-by-step**

## Notes

Add any observations or issues here:

_______________________________________________________________

_______________________________________________________________

_______________________________________________________________

---

**Refactoring Date:** _______________
**Tested By:** _______________
**Status:** [ ] Success  [ ] Needs Review  [ ] Failed
**Next Steps:** _______________________________________________
