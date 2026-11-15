# Bike Shop Parts & Tools Finder

A mobile-friendly web application to help bike shop mechanics find parts and tools in the shop layout.

## Features

- **Live Search**: Type to instantly search for parts and tools by name (e.g., "brakes", "tools")
- **Interactive Map**: 
  - Tap on any location to see what items are stored there
  - Zoom and pan to navigate the map
  - Locations are highlighted when search results match
  - Selected locations are shown with a red highlight
- **Mobile Optimized**: Designed for touch interaction on mobile devices
- **Static Files Only**: No server-side backend required - uses pure JavaScript and SVG

## Files

- `find.html` - Main application file (open this in a web browser)
- `bikeshop1.svg` - SVG map of the bike shop layout
- `mapkey.tsv` - Tab-separated values file mapping locations to items

## How to Use

1. **Open the Application**: Open `find.html` in a web browser
   - You can open it locally by dragging the file to your browser
   - Or serve it locally with a web server (e.g., `python3 -m http.server 8000`)

2. **Search for Items**:
   - Type in the search box at the top (e.g., "brakes", "tools", "tubes")
   - Results appear instantly as you type
   - Matching locations are highlighted in yellow on the map
   - Results are shown in an overlay panel

3. **Browse Locations**:
   - Tap on any location box on the map to see all items stored there
   - The location details appear in an overlay panel at the bottom

4. **Navigate the Map**:
   - **Desktop**: Use mouse wheel to zoom, click and drag to pan
   - **Mobile**: Pinch to zoom, drag with one finger to pan
   - Click the "×" button or tap outside to close the overlay

## Data Format

### mapkey.tsv
Tab-separated file with columns:
- `Location` - Location code (e.g., A2, B5, C3)
- `Part` - Name of the item stored there

### bikeshop1.svg
SVG drawing containing rectangles for each location, each with an ID matching the location code.

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile, etc.)
- Requires JavaScript enabled

## Notes

- The application loads both the SVG map and the TSV data file via HTTP requests
- For local use without a web server, you may encounter CORS issues; use a simple HTTP server as shown above
- Searches are case-insensitive and match partial words
