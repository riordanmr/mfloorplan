# Bike Shop Parts & Tools Finder - Quick Start Guide

## What Was Created

The web application has been created in the `/webapp` folder with the following files:

### Main Application
- **find.html** - The main web application (650 lines of HTML, CSS, and JavaScript)

### Data Files
- **bikeshop1.svg** - SVG map of the bike shop layout (copied from data/)
- **mapkey.tsv** - Location-to-parts mapping (copied from data/)

### Documentation & Utilities
- **README.md** - Full documentation
- **start.sh** - Quick start script to run the web server

## How to Use the Application

### Option 1: Using the Start Script (Recommended)
```bash
cd /Users/mrr/Documents/GitHub/mfloorplan/webapp
./start.sh
```
Then open http://localhost:8000/find.html in your browser.

### Option 2: Manual Web Server
```bash
cd /Users/mrr/Documents/GitHub/mfloorplan/webapp
python3 -m http.server 8000
```
Then open http://localhost:8000/find.html in your browser.

### Option 3: Direct File Opening
Simply open `find.html` directly in your browser (though some features may have limitations).

## Features Implemented

✅ **Live Search** - Type to search for parts/tools as you type
✅ **Highlighting** - Matching locations highlighted in yellow on the map
✅ **Location Selection** - Tap any location to see what's stored there (highlighted in red)
✅ **Zoom & Pan** - Mouse wheel to zoom, drag to pan (works on mobile too with pinch/drag)
✅ **Mobile Optimized** - Touch-friendly interface with fixed search bar
✅ **Results Overlay** - Clean overlay panel at bottom showing search results or location details
✅ **No Backend** - Pure JavaScript/SVG - static files only

## Technical Details

- **Technology**: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Data Loading**: Asynchronous fetch of SVG and TSV files
- **Search Algorithm**: Live filtering with case-insensitive partial matching
- **Map Interaction**: Native SVG manipulation with CSS classes
- **Zoom/Pan**: Using SVG CSS transforms (mouse wheel and touch support)
- **Mobile**: Responsive design with touch event handling

## Search Examples

Try searching for:
- "brakes" - finds all brake-related items
- "tools" - finds tool locations
- "tubes" - finds bike tubes
- "hub" - finds hub-related parts
- "cable" - finds cable and related items

## Original Files

✅ No modifications to existing files
✅ bikeshop1.html remains unchanged in the data/ folder
✅ All original data files untouched

## Browser Support

- Chrome/Edge 60+
- Firefox 55+
- Safari 12+
- Mobile browsers (iOS Safari, Chrome Mobile, etc.)
