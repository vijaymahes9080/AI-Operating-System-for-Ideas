# CLI Design & Interface

IdeasOS is fully operable via a Command Line Interface (**`ideas-os`**). This utility allows developers to script ingestion pipelines, query tasks, and manage agent runs from their terminal.

---

## 1. Global CLI Command Directory

```
                  ideas-os <command> [options]
```

| Command | Arguments | Options | Purpose |
|---|---|---|---|
| **`init`** | `[path]` | `--name <str>` | Scaffolds a new project directory. |
| **`inbox`** | `<filepath/url>` | `--type <enum>` | Ingests a new input file into the active project. |
| **`graph`** | `query <cypher>` | `--format <json/table>`| Queries the local knowledge graph database. |
| **`agent`** | `run <agent_id>` | `--task <str>` | Instructs a specialized agent to execute a task. |
| **`tasks`** | `list` | `--status <enum>` | Lists active workflow tasks for the workspace. |
| **`export`** | `[path]` | `--format <json/zip>` | Packages workspace data for portability. |

---

## 2. Programmatic Input Piping (CLI Standard Input)

The CLI supports standard Unix piping, allowing developers to write scripts that connect shell outputs to the IdeasOS inbox.

### Example: Pipe text output from git logs into the inbox
```bash
git log -n 5 | ideas-os inbox --type TEXT --title "Recent Code Changes"
```

### Example: Ingest all research files in a directory using a bash loop
```bash
find ./papers -name "*.pdf" | while read -r file; do
    ideas-os inbox "$file" --type PDF
done
```

---

## 3. Formatting Outputs

The CLI provides two output formats controlled by the `--format` flag:

1. **`table`** (Default): Uses character grid lines for terminal legibility.
2. **`json`**: Outputs raw minified JSON suitable for scripting with `jq`.

```bash
$ ideas-os tasks list --status IN_PROGRESS --format table

+------------------+-----------------------------+----------+------------+
| TASK ID          | TITLE                       | PRIORITY | ASSIGNEE   |
+------------------+-----------------------------+----------+------------+
| node_t_4892c90f  | Configure SQLite-vec DB     | HIGH     | coder_agent|
| node_t_57d29e81  | Run Playwright E2E tests    | MEDIUM   | qa_agent   |
+------------------+-----------------------------+----------+------------+
```

---

## 4. CLI Argument Parser Implementation

Below is the entrypoint configuration for Python's `argparse` router:

```python
# backend/app/cli.py
import argparse
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser(description="IdeasOS Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init
    init_parser = subparsers.add_parser("init", help="Scaffold a new project workspace")
    init_parser.add_argument("path", nargs="?", default=".", help="Workspace path")
    init_parser.add_argument("--name", required=True, help="Name of the workspace")

    # Ingest
    ingest_parser = subparsers.add_parser("inbox", help="Ingest resource to Inbox")
    ingest_parser.add_argument("target", help="Filepath, raw text, or URL")
    ingest_parser.add_argument("--type", choices=["TEXT", "VOICE", "IMAGE", "PDF", "WEBSITE"], default="TEXT")
    ingest_parser.add_argument("--title", help="Optional title")

    # Graph
    graph_parser = subparsers.add_parser("graph", help="Query knowledge graph")
    graph_sub = graph_parser.add_subparsers(dest="graph_action")
    query_parser = graph_sub.add_parser("query", help="Execute Cypher statement")
    query_parser.add_argument("statement", help="Cypher query string")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if not args.command:
        print("Error: No command specified. Use --help to view choices.")
        sys.exit(1)
        
    # Router execution logic...
    print(f"Executing: {args.command}")

if __name__ == "__main__":
    main()
```
