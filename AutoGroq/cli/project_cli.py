import argparse
import os
import json
from AutoGroq.project_manager import ProjectManager

def main():
    parser = argparse.ArgumentParser(description="Project Manager CLI")
    parser.add_argument("action", choices=["list", "create", "load", "save", "export", "import"], help="Action to perform")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--metadata", help="Project metadata as JSON string")
    parser.add_argument("--export_path", help="Path to export zip file")
    parser.add_argument("--import_zip", help="Path to import zip file")
    args = parser.parse_args()

    pm = ProjectManager()

    if args.action == "list":
        projects = pm.list_projects()
        print("Projects:", projects)

    elif args.action == "create":
        if not args.name:
            print("Project name required for create.")
            return
        metadata = json.loads(args.metadata) if args.metadata else None
        path = pm.create_project(args.name, metadata)
        print(f"Created project at {path}")

    elif args.action == "load":
        if not args.name:
            print("Project name required for load.")
            return
        data = pm.load_project(args.name)
        print(json.dumps(data, indent=2))

    elif args.action == "save":
        if not args.name:
            print("Project name required for save.")
            return
        # For demo, just reload and save back (simulate update)
        data = pm.load_project(args.name)
        pm.save_project(args.name, data["metadata"], data["chat_history"], data["agent_state"])
        print(f"Saved project {args.name}")

    elif args.action == "export":
        if not args.name or not args.export_path:
            print("Project name and export_path required for export.")
            return
        zip_path = pm.export_project(args.name, args.export_path)
        print(f"Exported project to {zip_path}")

    elif args.action == "import":
        if not args.import_zip:
            print("import_zip required for import.")
            return
        path = pm.import_project(args.import_zip)
        print(f"Imported project to {path}")

if __name__ == "__main__":
    main()