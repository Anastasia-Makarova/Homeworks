from setuptools import setup

setup(name="clean_folder",
      version="0.1.0",
      description="File sorter for a folder",
      author="Stacy",
      author_email="nastasia.makarova@gmail.com",
      url="https://github.com/Anastasia-Makarova/Homeworks/tree/main",
      license="MIT",
      entry_points = {"console_scripts":["clean-folder = clean_folder.clean_folder:main"]}
      )
