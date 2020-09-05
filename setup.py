from distutils.core import setup
from components import __version__

import os

def get_font_paths():
    font_paths = []
    for path, directories, filenames in os.walk("fonts"):
        for filename in filenames:
            font_paths.append(os.path.join(path, filename))

    return font_paths

setup(
    name="PyGame Objects",
    version=__version__,
    author="Chad Estioco",
    author_email="chadestioco@gmail.com",
    url="https://github.com/skytreader/PyGame-Objects",
    packages=["components", "components.helpers"],
    data_files=[("pygame-fonts", get_font_paths())],
    install_requires=["pygame"],
    license="MIT",
    description="PyGame Framework"
)
