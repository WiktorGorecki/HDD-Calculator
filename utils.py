import importlib
import os
import importlib.util


def run_plugin(plugin_path):
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
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py"):
                plugins.append(os.path.join(plugin_folder, filename))
    return plugins
