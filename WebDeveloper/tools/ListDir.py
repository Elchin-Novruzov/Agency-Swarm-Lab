from pydantic import Field

from agency_swarm import BaseTool
import os


class ListDir(BaseTool):
    """
    This tool returns the tree structure of the directory.
    """
    dir_path: str = Field(
        ..., description="Path of the directory to read.",
        examples=["./", "./test", "../../"]
    )

    def run(self):
        import os

        if not self.shared_state.get('app_directory'):
            return "You must create an app first to use this tool."

        if self.shared_state.get('app_directory') not in os.getcwd():
            return "You must be in the root directory of the app to use this tool."

        tree = []
        def list_directory_tree(path, indent=''):
            """Recursively list the contents of a directory in a tree-like format."""
            if not os.path.isdir(path):
                raise ValueError(f"The path {path} is not a valid directory")

            items = os.listdir(path)
            # exclude common hidden files and directories
            exclude = ['.git', '.idea', '__pycache__', 'node_modules',
                       '.DS_Store', '.vscode', '.next', 'dist', 'build', 'out']
            items = [item for item in items if item not in exclude]

            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                if i < len(items) - 1:
                    tree.append(indent + '├── ' + item)
                    if os.path.isdir(item_path):
                        list_directory_tree(item_path, indent + '│   ')
                else:
                    tree.append(indent + '└── ' + item)
                    if os.path.isdir(item_path):
                        list_directory_tree(item_path, indent + '    ')

        list_directory_tree(self.dir_path)

        return "\n".join(tree)

