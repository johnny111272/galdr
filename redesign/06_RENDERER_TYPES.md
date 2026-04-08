# Renderer Types

## How Renderers Fit In

The resolver determines what type of rendering is needed. The renderer produces the actual text. Each renderer takes exactly the inputs IT needs — simple renderers get a string, complex renderers get all four axes for their specific data shape.

## Simple Renderers

### Plain text
Takes a resolved string. Returns it as-is. Used for prose blobs, resolved variants, interpolated templates — anything that's already text after resolution.

### Heading
Takes a string and a heading level. Returns a markdown heading. Level 2 for sections, level 3 for groups within sections, level 4 for entries within groups.

## List Renderers

### Simple list
Takes a list of strings and a format specification (bulleted, numbered, inline). If the format has a threshold, uses item count to pick which format applies. Returns the formatted list.

### Templated entry list
Takes a list of item dictionaries and an entry template string. For each item, interpolates the template with that item's field values. Returns the formatted list of interpolated entries.

## Compound Renderers

These handle structured data with per-item logic. Each one is specific to a data shape because different shapes have genuinely different rendering needs.

### Enum-discriminated items
Data items have an enum field that determines which content templates apply per item. The renderer finds the enum value for each item, looks up the matching templates from a content sub-table group, interpolates with per-item values (including computed values like item index and total count), and renders the body text.

### Nested groups
Data items contain sub-items (groups with entries). The renderer handles per-group headings, per-group gates (should entry headings show? how many entries to render?), group framing content, and per-entry rendering with display format controls. Multiple levels of nesting — group level and entry level — each with their own heading format, separators, and containers from display.

### Variant-framed items
Data items have scalar fields plus a sub-list, and the content section provides per-item variant framing. The renderer resolves variant texts per item, interpolates with per-item field values, formats the sub-list per display settings, and assembles the framed output.

## Key Principle

The renderer set is determined by the data. We build a renderer for each distinct data shape that exists in the schemas. We don't build renderers speculatively. The schema review reveals what shapes exist, and each shape that needs specialized rendering gets its own renderer.

## Reference Data

### Shape Detection

The data field's annotation type determines its shape:

1. Gate (boolean/enum) → skip, no rendering
2. Nested BaseModel → skip, handled separately
3. Scalar → plain text rendering
4. List of scalars → simple list rendering
5. List of compound items → specialized renderer, determined by item structure:
   - Has entry template in content → templated entry list
   - Item has enum discriminator field → enum-discriminated
   - Item has nested sub-list of compound items → nested groups
   - Item has scalar sub-list → variant-framed
   - Fallback → nested groups

### Co-Occurrence Matrix

What cross-axis controls actually exist for each data trunk. This is reference data from analyzing the current schemas — it shows which trunks have labels, postscripts, entry templates, display formats, thresholds, or per-item variants.

See `review/` files for the current per-section field inventories.
