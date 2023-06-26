import importlib
import json
import os
import importlib.util


def run_plugin(plugin_path):
    print(plugin_path)
    plugin_name = os.path.splitext(os.path.basename(plugin_path))[0]
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run()

    if result:
        print("\nReturned result from the plugin: ", result)
        return result


def load_plugins():
    plugin_folder = "plugins"
    plugins = []

    if os.path.isdir(plugin_folder):
        for folder_name in os.listdir(plugin_folder):
            folder_path = os.path.join(plugin_folder, folder_name)
            if os.path.isdir(folder_path):
                plugin_data_file = os.path.join(folder_path, "info.json")
                if os.path.exists(plugin_data_file):
                    with open(plugin_data_file, "r") as f:
                        plugin_data = json.load(f)
                        display_name = plugin_data.get("display_name")
                        if display_name:
                            plugins.append((folder_path, display_name))

    return plugins
