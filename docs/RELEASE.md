# RELEASE Instructions — RobotSimulator

## Pre-Release Checklist

Before publishing a new version to GitHub:

### 1. Update VERSION File
```bash
# Edit VERSION file with new semantic version
echo "0.3.0" > VERSION
```

### 2. Update CHANGELOG.md
- Add entry for new version with date
- List all Added, Changed, Fixed, Removed items
- Update "Future Releases" section

### 3. Update Version in Code
- `robotsimulator/version.py` — automatically reads from VERSION file
- `app.py` — displays version dynamically from module
- Verify with: `python -c "from robotsimulator import VERSION; print(VERSION)"`

### 4. Run All Tests
```bash
cd /root/RobotSimulator
pytest tests/ -v
# Expected: 68 tests passing
```

### 5. Verify Import and Version Display
```bash
python -c "from robotsimulator import VERSION, VERSION_STRING; print(VERSION_STRING)"
# Expected: "0.3.0 (build YYYY-MM-DD)"
```

### 6. Test Streamlit App Launch
```bash
streamlit run app.py
# Verify version displays correctly in header and sidebar
# Verify disclaimer expander is visible
```

### 7. Generate Fresh Engineering Report
- Run app with sample data
- Generate report
- Verify report includes version and date

### 8. Commit Changes
```bash
git add VERSION CHANGELOG.md README.md
git commit -m "Release v0.3.0 — [brief description]"
git tag -a v0.3.0 -m "Version 0.3.0 release"
```

### 9. Push to GitHub
```bash
git push origin main --tags
```

### 10. Create GitHub Release
- Go to https://github.com/BotteroGroup/RobotSimulator/releases
- Click "Create a new release"
- Tag: v0.3.0
- Title: RobotSimulator v0.3.0
- Description: Copy from CHANGELOG.md
- Attach binaries if applicable

---

## GitHub Repository Setup (One-Time)

1. **Create repository** at https://github.com/new
   - Name: `RobotSimulator`
   - Organization: `BotteroGroup` (or personal)
   - Visibility: Private (recommended for proprietary) or Public

2. **Initialize with README**
   ```bash
   cd /root/RobotSimulator
   git init
   git remote add origin https://github.com/BotteroGroup/RobotSimulator.git
   git add .
   git commit -m "Initial release v0.2.0"
   git push -u origin main
   ```

3. **Enable GitHub Actions** (optional, for CI)
   - Create `.github/workflows/ci.yml`
   - Run tests on push/pull request

4. **Set repository topics**
   - Add topics: `robotics`, `fanuc`, `glass-manufacturing`, `trajectory-planning`

---

## Post-Release

- Test installation from GitHub on clean environment
- Verify all documentation links work
- Update internal wiki/documentation with new version