# Plan: Persistent Project-Based Workspaces with Export/Import

## 1. Project Structure

- Each project has its own directory:  
  `/projects/{project_name}/`
- Inside each project directory:
  - `files/` — All user-generated or modified files.
  - `chat_history.json` — Stores chat history.
  - `agent_state.json` — Stores agent state (variables, config, etc.).
  - `metadata.json` — Stores project metadata (name, creation date, etc.).

## 2. Persistence Mechanisms

- **Project Files:**  
  All files are saved in the `files/` subdirectory. File operations (create, edit, delete) are performed directly on disk.
- **Chat History:**  
  On each message, append to `chat_history.json`. On project load, read and display this history.
- **Agent State:**  
  Serialize agent state to `agent_state.json` on change or at session end. Load on project start.

## 3. Project Management Functions

- **Create Project:** Initialize directory and all JSON files.
- **Load Project:** Read all state from disk and populate session.
- **Save Project:** Write current state to disk.
- **Switch Project:** Save current, load selected.
- **List Projects:** Show available projects for selection.
- **Export Project:** Zip the entire project directory for download or backup.
- **Import Project:** Unzip a provided archive into the projects directory, making it available for use.

## 4. UI/UX Flow

- On app start, prompt user to select or create a project.
- All work is scoped to the selected project.
- User can switch projects at any time (with save/load).
- Export/import options available in the project management UI.

## 5. Implementation Steps

1. Design project directory structure.
2. Implement project CRUD (create, load, save, switch, list).
3. Refactor file operations to use project-scoped directories.
4. Add chat history and agent state serialization/deserialization.
5. Add export/import functionality using zip files.
6. Update UI to support project selection, switching, export, and import.

---

## Mermaid Diagram: Project Persistence Architecture

```mermaid
flowchart TD
    A[App Start] --> B{Select/Create Project}
    B --> C[Load Project State]
    C --> D[Session State (in-memory)]
    D --> E[User Interacts (chat, code, agents)]
    E --> F[Update Session State]
    F --> G[Persist Changes to Disk]
    G -->|chat, agent, files| H[Project Directory]
    H --> I[chat_history.json]
    H --> J[agent_state.json]
    H --> K[files/]
    H --> L[metadata.json]
    B --> M[List Projects]
    E --> N[Switch Project]
    N --> O[Save Current State]
    O --> B
    H --> P[Export/Import as Zip]
```

---

## Summary Table

| Component         | Persistence File         | Description                        |
|-------------------|-------------------------|------------------------------------|
| Project Files     | `files/`                | All user files per project         |
| Chat History      | `chat_history.json`     | Full chat transcript               |
| Agent State       | `agent_state.json`      | Serialized agent variables/config  |
| Project Metadata  | `metadata.json`         | Name, timestamps, etc.             |
| Export/Import     | `.zip` archive          | Full project backup/restore        |

---

**This plan provides a robust, user-friendly, and fully persistent project workspace system, including export/import for backup and portability.**