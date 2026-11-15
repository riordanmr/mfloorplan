# Bike Shop Parts & Tools Finder - File Index

## Quick Navigation

### Start Here
- **[README.md](README.md)** - User guide with all features explained
- **[QUICKSTART.md](QUICKSTART.md)** - How to run the application quickly

### Use the App
- **[find.html](find.html)** - The actual web application (open this!)

### For Developers
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Technical documentation, architecture, and design notes

### Supporting Files
- **[bikeshop1.svg](bikeshop1.svg)** - SVG map of the shop
- **[mapkey.tsv](mapkey.tsv)** - Location-to-items data mapping
- **[start.sh](start.sh)** - Helper script to run the web server

---

## Getting Started in 30 Seconds

1. Open Terminal and navigate to this folder:
   ```bash
   cd /Users/mrr/Documents/GitHub/mfloorplan/webapp
   ```

2. Start the web server:
   ```bash
   ./start.sh
   ```
   
   Or manually:
   ```bash
   python3 -m http.server 8000
   ```

3. Open your browser and go to:
   ```
   http://localhost:8000/find.html
   ```

4. Start searching! Type in the search box at the top.

---

## File Purposes

| File | Purpose | Size |
|------|---------|------|
| find.html | Main application with all code | 22 KB |
| bikeshop1.svg | Shop layout map | 10 KB |
| mapkey.tsv | Location-to-parts mapping | 1.3 KB |
| README.md | User documentation | 2.3 KB |
| QUICKSTART.md | Quick start guide | 2.5 KB |
| DEVELOPMENT.md | Technical documentation | 5.9 KB |
| start.sh | Web server startup script | 350 B |
| **Total** | **Complete application** | **60 KB** |

---

## What Can You Do?

✅ **Search** - Type to find any part or tool  
✅ **Highlight** - See all matching locations on the map  
✅ **Tap Locations** - Click any location to see what's there  
✅ **Zoom & Pan** - Navigate the map with zoom and scroll  
✅ **Mobile Ready** - Works perfectly on phones and tablets

---

## Questions?

- How do I use it? → Read [README.md](README.md)
- How do I start it? → Read [QUICKSTART.md](QUICKSTART.md)
- How does it work? → Read [DEVELOPMENT.md](DEVELOPMENT.md)

---

**Created:** November 14, 2026  
**Technology:** HTML5 + CSS3 + JavaScript (no backend required)  
**Browser Support:** Chrome, Firefox, Safari, Edge (desktop & mobile)
