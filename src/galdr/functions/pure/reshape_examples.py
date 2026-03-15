"""Reshape examples section: rename example_* fields to template names."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import Examples, ExampleGroup, ExampleEntry
from galdr.structures.template_context import (
    ExampleEntryContext,
    ExampleGroupContext,
    ExamplesContext,
)


def reshape_examples(examples: Examples | None) -> ExamplesContext | None:
    """Rename example_group_name/example_heading/etc to short names."""
    if examples is None:
        return None
    return ExamplesContext(
        groups=[reshape_group(group) for group in examples.groups.root],
    )


def reshape_group(group: ExampleGroup) -> ExampleGroupContext:
    """Reshape a single example group."""
    max_entries = unwrap(group.examples_max_number) if group.examples_max_number is not None else None
    return ExampleGroupContext(
        group_name=unwrap(group.example_group_name),
        display_headings=unwrap(group.example_display_headings),
        max_entries=max_entries,
        entries=[reshape_entry(entry) for entry in group.example_entries.root],
    )


def reshape_entry(entry: ExampleEntry) -> ExampleEntryContext:
    """Reshape a single example entry."""
    return ExampleEntryContext(
        heading=unwrap(entry.example_heading),
        text=unwrap(entry.example_text),
    )
