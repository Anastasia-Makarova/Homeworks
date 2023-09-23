import os
from pathlib import Path
import shutil
import sys
import zipfile


CATEGORIES = {"Audio": [".mp3", ".wav", ".flac", ".wma", ".ogg", ".amr"],
              "Docs": [".txt", ".doc", ".docx", ".xls", ".xlsx", ".pdf", ".ppt", ".pptx"],
              "Images": [".jpg", ".jpeg",".png", ".svg", ".raf"],
              "Video": [".mp4", ".mpeg", ".avi", ".mov", ".mkv"],
              "Archives": [".zip", ".gz", ".tar"]}

map = {ord("А"): "A", 
       ord("Б"): "B", 
       ord("В"): "V", 
       ord("Г"): "G", 
       ord("Д"): "D", 
       ord("Е"): "E", 
       ord("Ж"): "ZH", 
       ord("З"): "Z", 
       ord("И"): "I", 
       ord("Й"): "Y", 
       ord("К"): "K", 
       ord("Л"): "L", 
       ord("М"): "M", 
       ord("Н"): "N", 
       ord("О"): "O", 
       ord("П"): "P", 
       ord("Р"): "R", 
       ord("С"): "S", 
       ord("Т"): "T", 
       ord("У"): "U", 
       ord("Ф"): "F", 
       ord("Х"): "KH", 
       ord("Ц"): "TS", 
       ord("Ч"): "CH", 
       ord("Ш"): "SH", 
       ord("Щ"): "SHCH", 
       ord("Ы"): "Y", 
       ord("Э"): "E", 
       ord("Ю"): "YU", 
       ord("Я"): "YA", 
       ord("а"): "a", 
       ord("б"): "b", 
       ord("в"): "v", 
       ord("г"): "g", 
       ord("д"): "d", 
       ord("е"): "e", 
       ord("ж"): "zh", 
       ord("з"): "z", 
       ord("и"): "i", 
       ord("й"): "y", 
       ord("к"): "k", 
       ord("л"): "l", 
       ord("м"): "m", 
       ord("н"): "n", 
       ord("о"): "o", 
       ord("п"): "p", 
       ord("р"): "r", 
       ord("с"): "s", 
       ord("т"): "t", 
       ord("у"): "u", 
       ord("ф"): "f", 
       ord("х"): "kh", 
       ord("ц"): "ts", 
       ord("ч"): "ch", 
       ord("ш"): "sh", 
       ord("щ"): "shch", 
       ord("ы"): "y", 
       ord("э"): "e", 
       ord("ю"): "yu", 
       ord("я"): "ya"
    
}


def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"
    

def extention_list(path):
    known_extentions = set()
    found_extentions = set()
       

    for lst in CATEGORIES.values():
        for ext in lst:
            known_extentions.add(ext)

    for element in path.glob("**/*"):
        if element.is_file():
            found_extentions.add(element.suffix.lower())
    
    sorted_extentions = found_extentions&known_extentions
    unknown_extentions = found_extentions^sorted_extentions

    print("\nExtentions sorted:\n", str(sorted_extentions))
    print("\nUnknown extentions:\n", str(unknown_extentions))


def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder does not exist. Try another path."
    
    normalize(path)
    sort_folder(path)
    remove_empty_folder(path)
    print("\nSorted folder structure:")
    report(path)
    extention_list(path)
    unpack(path)
    
    return "\nDone"


def move_file(file:Path, category:str, root_dir:Path) -> None:
        target_dir = root_dir.joinpath(category)
        if not target_dir.exists():
            target_dir.mkdir()
        new_path = target_dir.joinpath(file.name)
        file.replace(new_path)


def normalize(path:Path):
    try:
        for element in path.glob("**/*"):
            if element.is_file():
                name = str(element.name)
                name = name.translate(map)
                normalized_name = ""
                for letter in name:
                    if ord(letter) <= 31 or 33 <=ord(letter) <=44 or ord(letter) == 47 or 59 <= ord(letter) <= 64 or ord(letter) >= 123:
                        normalized_name += "_"
                    else:
                        normalized_name += letter
                element.rename(path.joinpath(normalized_name))
    except FileExistsError:
        os.remove(element)

def remove_empty_folder(path:Path):
    
    list_of_folders_to_del = list(path.glob("**"))[::-1]

    for element in list_of_folders_to_del:
        try:
            element.rmdir()
        except OSError:
            continue


def report(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            print("\n", element.stem,":")
            report(path.joinpath(element))
        else:
            print("    ", element.name)


def sort_folder(path:Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file (element, category, path)


def unpack(path:Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file() and (element.suffix == ".zip" or element.suffix == ".gz" or element.suffix == ".tar"):
            try:
                shutil.unpack_archive(path.joinpath("Archives").joinpath(element.name), path.joinpath("Archives").joinpath(element.stem))
            except shutil.ReadError:
                with zipfile.ZipFile(path.joinpath("Archives").joinpath(element.name), 'r') as zip_ref:
                    zip_ref.extractall(path.joinpath("Archives").joinpath(element.stem))


if __name__  == "__main__":
    # main()
    print(main())
