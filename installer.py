import os
import shutil

import PyInstaller.__main__
import yaml


def install(name, path_to_main, path_to_search):
    print(f'Installing {name} from {path_to_main} and using search path {path_to_search}')
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        '--name',
        name,
        '--paths',
        path_to_search
    ])


def load_config():
    with open('./installer_config.yml', 'r') as file:
        return yaml.safe_load(file)


def cleanup_build_dirs(name):
    # Get the directory where installer.py is located
    base_dir = os.path.dirname(os.path.realpath(__file__))
    # Append the relative path to the directory you want to delete
    dirs = [f'dist/{name}.app', f'build/{name}']
    for directory in dirs:
        dir_to_remove = os.path.join(base_dir, directory)
        # Check if the directory exists
        if os.path.exists(dir_to_remove):
            # Remove the directory and all its contents
            print(f'Removing {dir_to_remove} ...')
            shutil.rmtree(dir_to_remove)


if __name__ == '__main__':
    print(f'current directory: {os.getcwd()}')

    config = load_config()
    for artifact, artifact_config in config.items():
        install(
            artifact_config['name'],
            artifact_config['path_to_main'],
            artifact_config['path_to_search']
        )
        # clean up for the next installation run
        cleanup_build_dirs(artifact_config['name'])
