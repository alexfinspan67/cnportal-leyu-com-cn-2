from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

SAMPLE_KEYWORD = "乐鱼体育"
SAMPLE_URL = "https://cnportal-leyu.com.cn"

@dataclass
class KeywordNote:
    """A single note entry for a keyword, with optional URL and tags."""
    keyword: str
    content: str
    source_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def summary(self) -> str:
        """Return a one-line summary of the note."""
        tag_part = f" [{', '.join(self.tags)}]" if self.tags else ""
        url_part = f" from {self.source_url}" if self.source_url else ""
        return f"{self.keyword}: {self.content[:40]}...{tag_part}{url_part}"


@dataclass
class KeywordNotesCollection:
    """A collection of keyword notes with export and formatting helpers."""
    notes: List[KeywordNote] = field(default_factory=list)
    title: str = "Untitled Notes"

    def add_note(self, keyword: str, content: str,
                 source_url: Optional[str] = None,
                 tags: Optional[List[str]] = None) -> None:
        """Add a new KeywordNote to the collection."""
        note = KeywordNote(
            keyword=keyword,
            content=content,
            source_url=source_url,
            tags=tags or []
        )
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return all notes matching the given keyword (case-insensitive)."""
        return [n for n in self.notes if n.keyword.lower() == keyword.lower()]

    def format_bullet_list(self) -> str:
        """Return a bullet-point formatted string of all notes."""
        if not self.notes:
            return f"## {self.title}\n(No notes yet.)"
        lines = [f"## {self.title}"]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. {note.summary()}")
        return "\n".join(lines)

    def format_markdown_table(self) -> str:
        """Return notes as a Markdown table."""
        if not self.notes:
            return f"**{self.title}** — empty"
        header = "| # | Keyword | Content (truncated) | Source | Tags |"
        separator = "|---|---------|---------------------|--------|------|"
        rows = []
        for i, note in enumerate(self.notes, 1):
            kw = note.keyword
            content = note.content[:50] + "..." if len(note.content) > 50 else note.content
            url = note.source_url or ""
            tags = ", ".join(note.tags) if note.tags else ""
            rows.append(f"| {i} | {kw} | {content} | {url} | {tags} |")
        return "\n".join([header, separator] + rows)

    def export_notes(self, output_format: str = "text") -> str:
        """Export notes in given format: 'text', 'bullets', or 'markdown'."""
        if output_format == "bullets":
            return self.format_bullet_list()
        elif output_format == "markdown":
            return self.format_markdown_table()
        else:
            # default text
            lines = [f"Collection: {self.title}"]
            for note in self.notes:
                lines.append(f"* {note.keyword}: {note.content}")
                if note.source_url:
                    lines.append(f"  URL: {note.source_url}")
                if note.tags:
                    lines.append(f"  Tags: {', '.join(note.tags)}")
                lines.append("---")
            return "\n".join(lines)


def sample_notes() -> KeywordNotesCollection:
    """Create a small collection with sample data for testing."""
    collection = KeywordNotesCollection(title="Keyword Observation Log")
    collection.add_note(
        keyword=SAMPLE_KEYWORD,
        content="This is a sample note for the keyword 乐鱼体育, demonstrating dataclass usage.",
        source_url=SAMPLE_URL,
        tags=["sample", "demo"]
    )
    collection.add_note(
        keyword="运动",
        content="General sports keyword — used for broader coverage.",
        tags=["sports"]
    )
    collection.add_note(
        keyword="数据报告",
        content="Quarterly analysis report for user engagement metrics.",
        source_url="https://example.com/report",
        tags=["analytics", "internal"]
    )
    return collection


def main():
    """Run a quick demonstration of the KeywordNotesCollection."""
    notes = sample_notes()
    print("=== Bullet List ===")
    print(notes.format_bullet_list())
    print("\n=== Markdown Table ===")
    print(notes.format_markdown_table())
    print("\n=== Text Export ===")
    print(notes.export_notes("text"))
    # Demonstrate lookup
    found = notes.find_by_keyword("乐鱼体育")
    if found:
        print(f"\nFound {len(found)} note(s) matching '乐鱼体育'")
        for n in found:
            print(f"  -> {n.content}")


if __name__ == "__main__":
    main()