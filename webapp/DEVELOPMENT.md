# Development Notes

## Architecture

The Bike Shop Finder is a single-page JavaScript application with the following architecture:

```
find.html
  ├── HTML Structure
  │   ├── Header (Search bar + Clear button)
  │   ├── Map Container (SVG + Overlay panel)
  │   └── Overlay (Search results or location details)
  │
  ├── CSS Styles (responsive, mobile-optimized)
  │
  └── JavaScript (all logic)
      ├── Data Loading
      │   ├── loadSvg() - Fetch and parse SVG
      │   └── loadTsvData() - Parse TSV mapping
      │
      ├── UI Management
      │   ├── setupEventListeners() - Keyboard & button events
      │   ├── setupPanZoom() - Map interaction (zoom, pan)
      │   └── setupLocationInteractions() - Click handlers
      │
      ├── Search Logic
      │   └── handleSearch() - Live search filtering
      │
      └── Display Functions
          ├── showSearchResults() - Show search overlay
          ├── selectLocation() - Handle location tap
          ├── showLocationDetails() - Show location overlay
          └── closeOverlay() - Hide overlay
```

## Data Structures

### mapData Object
```javascript
mapData = {
  partsByLocation: {
    "A2": ["Tubes"],
    "A4": ["Brakes", "Brake levers", "Derailleurs", ...],
    "A7": ["Hubs", "Headset spacers", ...],
    ...
  },
  locationsByPart: {
    "brakes": [
      {location: "A4", part: "Brakes"},
      {location: "A8", part: "Brake pads"},
      ...
    ],
    "tubes": [
      {location: "A2", part: "Tubes"},
      {location: "G7", part: "Tubes"}
    ],
    ...
  }
}
```

### state Object
```javascript
state = {
  currentSearch: "",           // Current search query
  highlightedLocations: Set(), // Set of location IDs matching search
  selectedLocation: null,      // Currently selected location ID
  svgElement: null,           // Reference to SVG DOM element
  panzoom: null              // Pan/zoom state
}
```

## Key Functions

### Initialization
- `init()` - Bootstrap the application, load data, setup listeners
- `loadSvg()` - Fetch SVG file and inject into DOM
- `loadTsvData()` - Fetch and parse TSV file into data structures

### Interaction
- `handleSearch(query)` - Filter parts by search term, highlight locations
- `selectLocation(locationId)` - Show details for tapped location
- `setupPanZoom()` - Enable mouse wheel zoom and drag to pan

### UI Updates
- `showSearchResults(results)` - Display search matches in overlay
- `showLocationDetails(locationId, parts)` - Display location's items
- `showNoResults()` - Display "no results" message
- `closeOverlay()` - Hide overlay and deselect location

## CSS Classes Used

- `.highlighted` - Yellow background for search matches
- `.selected` - Red background for selected location
- `.location-rect` - Any clickable location rectangle
- `.active` - Overlay is visible

## Mobile Optimizations

1. **Touch Events**
   - Touch pan: Single finger drag
   - Pinch zoom: Two-finger pinch gesture
   - Tap to select: Single tap on location

2. **Responsive Design**
   - Fixed search bar stays visible while scrolling map
   - Overlay takes 50-60% of screen on mobile
   - Font sizes and padding adjusted for touch targets

3. **Performance**
   - Data structures optimized for fast lookups
   - CSS transforms used for smooth panning/zooming
   - No external dependencies

## Search Algorithm

1. User types in search box
2. `handleSearch()` converts query to lowercase
3. Iterate through `locationsByPart` keys
4. Find all parts where key includes query string (partial match)
5. Get all locations for matching parts
6. Highlight those locations on map
7. Show results in overlay

Example: Query "brake" matches:
- "brakes" → shows location A4
- "brake levers" → shows location A4
- "brake pads" → shows location A8
- "brake cables" → shows location C4

## Zoom & Pan Implementation

Uses SVG CSS transforms (`transform: translate() scale()`):

**Zoom:**
- Mouse wheel: Adjust scale, recalculate translate to zoom toward cursor
- Touch pinch: Calculate zoom ratio from finger distance, adjust accordingly

**Pan:**
- Mouse: Track mousedown/move/up, update translate
- Touch: Track touch start/move, update translate

Transform origin is always (0, 0) so all coordinates remain consistent.

## Browser API Usage

- `fetch()` - Load external files
- `Document.parseFromString()` - Parse SVG XML
- `querySelector()` / `querySelectorAll()` - DOM manipulation
- `classList` - Add/remove CSS classes
- Event listeners: `click`, `input`, `wheel`, `touch*`, `mouse*`
- `touch-action: none` - Prevent default browser touch behaviors

## Future Enhancement Ideas

1. **Favorites/Bookmarks** - Save frequently searched items
2. **Recent Searches** - Show history of searches
3. **Categories** - Group parts by type (e.g., "Brakes", "Cables", "Tools")
4. **Offline Mode** - Cache data for offline use
5. **Print Map** - Generate printable location guide
6. **Search Suggestions** - Autocomplete as user types
7. **Keyboard Navigation** - Arrow keys to select locations
8. **Export** - Save search results as list
9. **Multi-location Search** - Find items between two locations
10. **Analytics** - Track most searched items

## Known Limitations

1. SVG must be served via HTTP (file:// protocol has CORS restrictions)
2. No search history or preferences saved (stateless app)
3. No error recovery if data files are malformed
4. No keyboard shortcuts for advanced navigation
5. Pin/bookmark features not implemented

## Testing Checklist

- [ ] Search box accepts input
- [ ] Live search filters as you type
- [ ] Clear button resets search
- [ ] Search results show in overlay
- [ ] Location highlighting works
- [ ] Tapping location shows items stored there
- [ ] Overlay closes when clicking outside
- [ ] Map zoom works with mouse wheel
- [ ] Map pan works with drag
- [ ] Touch pinch zoom works on mobile
- [ ] Touch pan works on mobile
- [ ] Responsive layout on small screens
- [ ] No console errors
