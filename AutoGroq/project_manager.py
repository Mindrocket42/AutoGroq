import os
import json
import shutil
from typing import List, Dict, Optional
from zipfile import ZipFile

PROJECTS_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects")

class ProjectManager:
    def __init__(self, projects_root: Optional[str] = None):
        self.projects_root = projects_root or PROJECTS_ROOT
        os.makedirs(self.projects_root, exist_ok=True)

    def list_projects(self) -> List[str]:
        """List all project names."""
        return [
            name for name in os.listdir(self.projects_root)
            if os.path.isdir(os.path.join(self.projects_root, name))
        ]

    def create_project(self, project_name: str, metadata: Optional[Dict] = None) -> str:
        """Create a new project directory with initial files."""
        project_dir = os.path.join(self.projects_root, project_name)
        files_dir = os.path.join(project_dir, "files")
        os.makedirs(files_dir, exist_ok=True)
        # Initialize metadata
        metadata_path = os.path.join(project_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata or {"name": project_name}, f, indent=2)
        # Initialize chat history and agent state
        for fname in ["chat_history.json", "agent_state.json"]:
            with open(os.path.join(project_dir, fname), "w", encoding="utf-8") as f:
                json.dump([], f)
        return project_dir

    def load_project(self, project_name: str) -> Dict:
        """Load project metadata, chat history, and agent state."""
        project_dir = os.path.join(self.projects_root, project_name)
        with open(os.path.join(project_dir, "metadata.json"), "r", encoding="utf-8") as f:
            metadata = json.load(f)
        with open(os.path.join(project_dir, "chat_history.json"), "r", encoding="utf-8") as f:
            chat_history = json.load(f)
        with open(os.path.join(project_dir, "agent_state.json"), "r", encoding="utf-8") as f:
            agent_state = json.load(f)
        return {
            "metadata": metadata,
            "chat_history": chat_history,
            "agent_state": agent_state,
            "files_dir": os.path.join(project_dir, "files"),
        }

    def save_project(self, project_name: str, metadata: Dict, chat_history: List, agent_state: Dict):
        """Save project metadata, chat history, and agent state."""
        project_dir = os.path.join(self.projects_root, project_name)
        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        with open(os.path.join(project_dir, "chat_history.json"), "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2)
        with open(os.path.join(project_dir, "agent_state.json"), "w", encoding="utf-8") as f:
            def safe_json(obj):
                if hasattr(obj, "to_dict"):
                    return obj.to_dict()
                elif hasattr(obj, "__dict__"):
                    return obj.__dict__
                else:
                    return str(obj)
            json.dump(agent_state, f, indent=2, default=safe_json)

    def export_project(self, project_name: str, export_path: str) -> str:
        """Export the entire project directory as a zip file."""
        project_dir = os.path.join(self.projects_root, project_name)
        zip_path = os.path.join(export_path, f"{project_name}.zip")
        with ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(project_dir):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, project_dir)
                    zipf.write(abs_path, arcname=os.path.join(project_name, rel_path))
        return zip_path

    def import_project(self, zip_file_path: str) -> str:
        """Import a project from a zip file."""
        with ZipFile(zip_file_path, "r") as zipf:
            zipf.extractall(self.projects_root)
        # Return the name of the imported project
        project_name = os.path.splitext(os.path.basename(zip_file_path))[0]
        return os.path.join(self.projects_root, project_name)