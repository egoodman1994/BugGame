import PyInstaller.__main__
import os
import sys
import shutil

# Clean up old builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')
for file in os.listdir('.'):
    if file.endswith('.spec'):
        os.remove(file)

# Get absolute paths
root_dir = os.path.abspath(os.path.dirname(__file__))
assets_path = os.path.join(root_dir, "assets")
src_path = os.path.join(root_dir, "src")

PyInstaller.__main__.run([
    'bug-catching-cat.py',
    '--onefile',
    '--windowed',
    '--name=BugCatcher',
    f'--add-data={assets_path}{os.pathsep}assets',
    f'--add-data={src_path}{os.pathsep}src',
    f'--paths={root_dir}',
    '--hidden-import=pygame',
    '--hidden-import=src.game',
    '--hidden-import=src.sprites.player',
    '--hidden-import=src.sprites.bug',
    '--hidden-import=src.utils.constants',
    '--hidden-import=src.utils.leaderboard',
    '--hidden-import=src.utils.image_processor',
    '--debug=imports',
    '--clean',
    '--noconfirm'  # Don't ask for confirmation when cleaning
]) 