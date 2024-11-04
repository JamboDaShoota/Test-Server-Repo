import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Paths relative to the script's directory
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(PROJECT_FOLDER, "default.project.json")

class FolderHandler(FileSystemEventHandler):

    delete_list : dict = {}

    def on_created(self, event):
        if event.is_directory:  # Only act if a new folder is created
            relative_path = os.path.relpath(event.src_path, PROJECT_FOLDER)
            print(f"New folder detected: {relative_path}")

            # Update JSON model
            self.update_json_model(relative_path, False)

        else:
            relative_path = os.path.relpath(event.src_path, PROJECT_FOLDER)
            if (relative_path[-4:] == ".lua" or relative_path[-5:] == ".luau") and (relative_path.split(os.sep)[-1][:5] != "init."):
                print(f"New ModuleScript detected: {relative_path}")
                # Update JSON model
                self.update_json_model(relative_path, True)

    def on_deleted(self, event):
        relative_path : str = os.path.relpath(event.src_path, PROJECT_FOLDER)
        if event.is_directory:  # Only act if a folder is deleted
            print(f"Folder deleted: {relative_path}")

            # Update JSON model
            self.remove_from_json_model(relative_path)
        else:
            if (relative_path[-4:] == ".lua" or relative_path[-5:] == ".luau") and (relative_path.split(os.sep)[-1][:5] != "init."):
                print(f"ModuleScript deleted: {relative_path}")
                # Update JSON model
                self.remove_from_json_model(relative_path)

        self.delete_list[relative_path.split(os.sep)[-1]] = relative_path

    def update_json_model(self, relative_path, isFile : bool):
        # Load current JSON data
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)

        temp_path = relative_path[5:]

        # Split the relative path into parts for nested structure
        path_parts = temp_path.split(os.sep)

        # Get the top-level tree object
        current_level = data["tree"]

        # Traverse the tree and create any necessary nodes
        for part in path_parts:
            if part not in current_level:
                # Create a new folder node if it doesn't exist
                current_level[part] = {}
            # Move to the next level down in the tree
            current_level = current_level[part]

        # Update the path property for the newly added folder
        if isFile:
            current_level["$className"] = "ModuleScript"
        current_level["$path"] = os.path.join("game", *path_parts)

        # Write back the updated JSON data
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Updated JSON model with path: {relative_path}")


    def remove_from_json_model(self, relative_path):
        # Load current JSON data
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)

        temp_path = relative_path[5:] # this is to remove game from the path

        # Split the relative path into parts for nested structure
        path_parts = temp_path.split(os.sep)
        
        # Traverse the structure and remove the folder
        current_level = data["tree"]
        for part in path_parts[:-1]:  # Traverse to the parent folder
            if part in current_level:
                current_level = current_level[part]
            else:
                return  # If the folder doesn't exist, exit

        # Remove the folder or file 
        folder_to_remove = path_parts[-1]
        if folder_to_remove in current_level:
            del current_level[folder_to_remove]
            print(f"Removed folder/file from JSON model: {relative_path}")

        # Write back the updated JSON data
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)

def main():
    event_handler = FolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path=PROJECT_FOLDER, recursive=True)
    observer.start()
    print("Monitoring for new folders...")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print(f"Delete list\n{event_handler.delete_list}")
        event_handler.delete_list = None # Just double checking lol
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
