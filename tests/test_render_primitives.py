"""Tests for rendering primitives."""

from galdr.functions.pure.render_primitives import (
    bold_label,
    bold_label_code,
    code_block,
    heading,
    join_sections,
    list_as_bullets,
    list_as_numbered,
    list_as_prose,
    paragraph,
    section_frame,
    structured_entries,
    yaml_frontmatter,
)


# --- heading ---


def test_heading_h1():
    assert heading(1, "Title") == "# Title"


def test_heading_h2():
    assert heading(2, "Input") == "## Input"


def test_heading_h3():
    assert heading(3, "Group Name") == "### Group Name"


def test_heading_empty_text():
    assert heading(2, "") == ""


# --- list_as_bullets ---


def test_bullets_multiple():
    assert list_as_bullets(["a", "b", "c"]) == "- a\n- b\n- c"


def test_bullets_single():
    assert list_as_bullets(["only"]) == "- only"


def test_bullets_empty():
    assert list_as_bullets([]) == ""


# --- list_as_numbered ---


def test_numbered_multiple():
    assert list_as_numbered(["a", "b", "c"]) == "1. a\n2. b\n3. c"


def test_numbered_single():
    assert list_as_numbered(["only"]) == "1. only"


def test_numbered_empty():
    assert list_as_numbered([]) == ""


# --- bold_label ---


def test_bold_label_basic():
    assert bold_label("Purpose", "Do the thing") == "**Purpose:** Do the thing"


def test_bold_label_code_basic():
    assert bold_label_code("Schema", "/path/to/file") == "**Schema:** `/path/to/file`"


# --- code_block ---


def test_code_block_no_language():
    assert code_block("print('hi')") == "```\nprint('hi')\n```"


def test_code_block_with_language():
    assert code_block("echo hi", "bash") == "```bash\necho hi\n```"


def test_code_block_multiline():
    content = "line one\nline two"
    assert code_block(content) == "```\nline one\nline two\n```"


# --- paragraph ---


def test_paragraph_basic():
    assert paragraph("Hello world") == "Hello world"


def test_paragraph_empty():
    assert paragraph("") == ""


# --- join_sections ---


def test_join_sections_basic():
    assert join_sections(["a", "b"]) == "a\n---\nb"


def test_join_sections_filters_empty():
    assert join_sections(["a", "", "b"], "\n---\n") == "a\n---\nb"


def test_join_sections_all_empty():
    assert join_sections(["", "", ""]) == ""


def test_join_sections_custom_separator():
    assert join_sections(["a", "b"], "\n\n") == "a\n\nb"


# --- section_frame ---


def test_section_frame_full():
    result = section_frame("Rules", 2, "Follow these:", "Do not skip.", "- rule 1\n- rule 2")
    assert result == "## Rules\n\nFollow these:\n\nDo not skip.\n\n- rule 1\n- rule 2"


def test_section_frame_heading_and_content():
    result = section_frame("Rules", 2, "", "", "- rule 1")
    assert result == "## Rules\n\n- rule 1"


def test_section_frame_framing_no_warning():
    result = section_frame("Rules", 2, "Follow these:", "", "- rule 1")
    assert result == "## Rules\n\nFollow these:\n\n- rule 1"


def test_section_frame_empty_content():
    assert section_frame("Rules", 2, "framing", "warning", "") == ""


def test_section_frame_no_heading():
    result = section_frame("", 2, "", "", "content here")
    assert result == "content here"


# --- list_as_prose ---


def test_prose_multiple():
    assert list_as_prose(["Stay focused", "No hallucination"]) == "Stay focused. No hallucination."


def test_prose_single():
    assert list_as_prose(["Only this"]) == "Only this."


def test_prose_empty():
    assert list_as_prose([]) == ""


def test_prose_preserves_existing_punctuation():
    assert list_as_prose(["Already done.", "Question?", "Exclaim!"]) == "Already done. Question? Exclaim!"


# --- structured_entries ---


def test_structured_entries_standard():
    entries = [
        ("All records processed", ["Output file exists", "Record count matches"]),
        ("Schema valid", ["No validation errors"]),
    ]
    result = structured_entries(entries)
    assert "All records processed" in result
    assert "Evidence:" in result
    assert "- Output file exists" in result
    assert "- Record count matches" in result
    assert "Schema valid" in result
    assert "- No validation errors" in result


def test_structured_entries_compact():
    entries = [
        ("All records processed", ["Output file exists"]),
        ("Schema valid", ["No errors"]),
    ]
    result = structured_entries(entries, evidence_mode="compact")
    assert "- All records processed" in result
    assert "- Schema valid" in result
    assert "Evidence:" not in result
    assert "Output file exists" not in result


def test_structured_entries_empty():
    assert structured_entries([]) == ""


def test_structured_entries_single():
    entries = [("Done", ["File written"])]
    result = structured_entries(entries)
    assert "Done" in result
    assert "- File written" in result


# --- yaml_frontmatter ---


def test_yaml_frontmatter_basic():
    result = yaml_frontmatter({"name": "agent", "model": "opus"})
    assert result == '---\nname: "agent"\nmodel: "opus"\n---'


def test_yaml_frontmatter_empty():
    result = yaml_frontmatter({})
    assert result == "---\n---"
