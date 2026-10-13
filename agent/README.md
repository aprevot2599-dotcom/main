# BMCC Advising Agent

A command-line advising assistant for Blue Mountain Community College staff. Given a student's degree audit and a goal, it reads the BMCC catalog and advising material, researches transfer programs at other colleges, counts dual credit already earned, and fills out a term-by-term degree planning worksheet (Word) with the checks an advisor needs to review.

## Run it

```bash
pip install -r agent/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # or: ant auth login
python agent/agent.py
```

Example request: `Build a pathway for audits/student-a.pdf toward the AAOT, starting Fall 2026, then transfer to EOU for business. She has dual credit from Hermiston High.`

## Folders

| Folder | Holds | In git? |
| --- | --- | --- |
| `agent/library/` | Advising guides, 8 Term Degree Planner, worksheets, catalog excerpts, transfer maps | No |
| `agent/audits/` | Degree audit exports from the SIS (PDF, DOCX, TXT, CSV) | Never |
| `agent/worksheets/` | Completed planning worksheets (.docx) | Never |

## What it can use

| Tool | Purpose |
| --- | --- |
| `list_audits`, `read_audit` | Reads exported degree audits; masks SSN-shaped numbers, long ID numbers, emails and birth dates before Claude sees them |
| `list_library`, `read_library_document` | Reads local advising material |
| `web_search`, `web_fetch` | BMCC catalog (catalog.bluecc.edu), bluecc.edu advising and Early College Credit pages, other colleges' catalogs and transfer pages |
| `save_worksheet` | Writes the worksheet and flags terms over 18 credits, repeated courses and credit shortfalls |

The system prompt tells it to verify every course and credit against a source it read, cite those sources on the worksheet, and mark anything unverified "verify with advisor".

## Limits to know

- **No live SIS connection.** Audits come in as exported files. A direct connection needs the SIS vendor's API, credentials and IT approval.
- **Student data leaves campus.** Audit text is sent to the Claude API. Confirm BMCC's data agreement with Anthropic covers FERPA records before using real audits. The redaction is pattern-based and will miss names and anything unusual.
- **Worksheet layout is generic.** It is an 8-term-style plan, not BMCC's official form. Drop the official template in `library/` and the writer can be mapped to it.
- **Web content changes.** Catalog pages are read live; the catalog year the agent cites is the one it found, so check it matches the student's.

## Settings

Model `claude-opus-5-5` at effort `high`, since advising accuracy matters more than speed. Server-side refusal fallback is on (`fallbacks="default"`); remove those two lines in `run_turn` to turn it off.
