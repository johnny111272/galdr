# Migration: Current Jinja2 to L1 Composition Engine

**L1 target:** `galdr input.toml` with no CLI flags produces functionally equivalent output to the current Jinja2 system. No recipe or style files needed — the engine uses built-in defaults that reproduce current behavior.

**Verification method:** Render all existing agents through both old and new engines. Diff outputs. Differences must be whitespace-only or documented intentional improvements.

---

## Step 1: Rendering Primitives

Create `src/galdr/functions/pure/render_primitives.py`.

Pure functions, no dependencies beyond Python stdlib:
- `list_as_bullets(items) -> str`
- `list_as_numbered(items) -> str`
- `heading(level, text) -> str`
- `code_block(content) -> str`
- `section_frame(heading, framing, warning, content) -> str`
- `field_line(label, value) -> str`

Start with the primitives needed for current output. Additional primitives (prose, table, structured_entries) can be added when recipes demand them.

Test each primitive in isolation.

## Step 2: Models

Create recipe and style models in `src/galdr/structures/`:
- `recipe.py` — `RecipeConfig`, `ModuleConfig`
- `style.py` — `StyleConfig`, `StyleEntry`

Frozen Pydantic models. These describe the config shape. At L1 they are instantiated from hardcoded defaults, not loaded from files.

## Step 3: Default Recipe + Default Style

Create `src/galdr/functions/pure/defaults.py`.

Two functions:
- `default_recipe() -> RecipeConfig` — module list matching current standard_v1.md.j2 order
- `default_style() -> StyleConfig` — headings and framing matching current template text

These encode the current behavior as explicit config. When the engine uses them, output matches current output.

## Step 4: Section Renderers

Create `src/galdr/functions/pure/render_sections.py`.

One function per module:
- `render_frontmatter(data: FrontmatterContext) -> str`
- `render_identity(data: IdentityContext, style: StyleEntry, config: ModuleConfig) -> str`
- `render_constraints(data: ConstraintsContext, style: StyleEntry, config: ModuleConfig) -> str`
- ... etc for all 14 modules

Each function composes rendering primitives to produce its section's markdown. The current template logic translates directly — the conditionals, loops, and string interpolation move from Jinja2 syntax to Python.

## Step 5: Composition Engine

Create `src/galdr/functions/pure/compose.py`.

```python
def compose_agent(context: RenderContext, recipe: RecipeConfig, style: StyleConfig) -> str
```

Pure function. Iterates recipe modules, calls section renderers, joins results with separators. Handles:
- Locked positions (frontmatter first)
- Optional module skipping (None data)
- Separator insertion between sections

## Step 6: Wire Into Pipeline

Update `engine.py`:
- `render_agent(context)` calls `compose_agent(context, default_recipe(), default_style())`
- Remove Jinja2 imports
- Remove template loading
- `engine.py` becomes pure (no filesystem access for templates)

Update `pipeline.py` if needed (likely no changes — it calls `render_agent(context)`).

## Step 7: Verify Parity

Render all existing agents with the new engine. Compare against current staging outputs:
- `definitions/staging/interview-enrich-create-summary.md`
- `definitions/staging/embedding-normalize-combined-opus.md`
- ... all deployed agents

Diff each pair. Fix discrepancies until output matches or differences are documented improvements.

## Step 8: Clean Up

- Delete `src/galdr/templates/` directory entirely
- Remove `jinja2` from `pyproject.toml` dependencies
- Update `uv.lock`
- Commit clean state

After Step 8, L1 is complete. The system produces identical output with no Jinja2, and the architecture is ready for L2 (recipe file loading) and L3 (style file loading).
