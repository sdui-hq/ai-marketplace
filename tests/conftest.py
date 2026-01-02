"""pytest configuration - auto-discovers plugins and adds component paths."""

import sys
from pathlib import Path

PLUGIN_COMPONENTS = ["hooks", "skills", "commands", "lib"]

project_root = Path(__file__).parent.parent

# Directories to scan for plugins (root level and plugins/ subdirectory)
plugin_search_dirs = [project_root]
plugins_subdir = project_root / "plugins"
if plugins_subdir.exists():
    plugin_search_dirs.append(plugins_subdir)

for search_dir in plugin_search_dirs:
    for plugin_dir in search_dir.iterdir():
        if not plugin_dir.is_dir():
            continue
        if not (plugin_dir / ".claude-plugin").exists():
            continue

        for component in PLUGIN_COMPONENTS:
            component_path = plugin_dir / component
            if component_path.exists():
                sys.path.insert(0, str(component_path))
