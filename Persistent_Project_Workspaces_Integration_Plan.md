# Integration Plan: Persistent Project Workspaces in Streamlit

## 1. Project Directory Structure
- Each project will reside in `projects/{project_name}/` with:
  - `files/` (user files)
  - `chat_history.json`
  - `agent_state.json`
  - `metadata.json`

## 2. Persistence Mechanisms
- **File Operations:** All file actions (create, edit, delete) are performed in the `files/` subdirectory.
- **Chat History:** Each message is appended to `chat_history.json`. On project load, this is read and displayed.
- **Agent State:** Serialize to `agent_state.json` on change/session end; load on project start.
- **Metadata:** Store project name, creation date, etc., in `metadata.json`.

## 3. Project Management Functions (UI & Backend)
- **Create Project:** UI form to enter project name/metadata. Backend initializes directory and JSON files.
- **Load Project:** UI project selector. Backend loads all state from disk into session.
- **Save Project:** UI button to save current state to disk.
- **Switch Project:** UI selector. Backend saves current, loads selected project, and resets all session state.
- **List Projects:** UI displays all available projects for selection.
- **Export Project:** UI button to download a zip of the project directory.
- **Import Project:** UI file uploader to unzip a project archive into `projects/`.

## 4. UI/UX Flow
- On app start, prompt user to select or create a project.
- All work (chat, agent, files) is strictly scoped to the selected project.
- User can switch projects at any time (with save/load).
- Export/import options are available in the project management UI.

## 5. Implementation Steps
1. **Refactor Session State Management**
   - Ensure all state (chat, agent, files) is loaded from and saved to the selected project directory.
   - On project switch, clear and reload all relevant session state.
2. **Project CRUD Operations**
   - Implement backend functions for create, load, save, switch, list, export, and import.
   - Ensure atomicity and error handling for file operations.
3. **UI Enhancements**
   - Add a sidebar or modal for project selection/creation.
   - Add buttons for save, export, import, and switch.
   - Display current project metadata in the UI.
4. **File Management**
   - Refactor file upload/download features to operate within the current project's `files/` directory.
   - Ensure file browser (if present) is project-scoped.
5. **Chat & Agent State**
   - Refactor chat and agent logic to read/write from the current project's JSON files.
   - On project switch, reload chat and agent state from disk.
6. **Export/Import**
   - Implement zip/unzip logic for full project backup/restore.
   - UI for downloading/uploading project archives.
7. **Testing & Validation**
   - Test all flows: create, switch, save, export, import, and ensure strict project isolation.

## 6. Mermaid Diagram: Project Persistence Architecture

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

## 7. Summary Table

| Component         | Persistence File         | Description                        |
|-------------------|-------------------------|------------------------------------|
| Project Files     | `files/`                | All user files per project         |
| Chat History      | `chat_history.json`     | Full chat transcript               |
| Agent State       | `agent_state.json`      | Serialized agent variables/config  |
| Project Metadata  | `metadata.json`         | Name, timestamps, etc.             |
| Export/Import     | `.zip` archive          | Full project backup/restore        |

---

**All state (chat, agent, files) will be fully decoupled per project, and the UI will support the complete project management flow as described.**