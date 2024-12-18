# Davinci Resolve Automatic Import Script

~~I need Track, why does Blackmagic sleep so long~~

## Project Introduction

This project aims to automate the import of time-coded audio files (WAV format) into DaVinci Resolve and organize them according to a predefined folder structure. The main features include:

1. **Import Audio Files**: Recursively scan the specified folder for WAV files and import them into DaVinci Resolve's media pool.
2. **Organize Media Items**: Automatically assign characters and tracks based on the audio file's folder structure to avoid timecode overlaps.
3. **Timecode Management**: Handle time-coded audio files to ensure proper synchronization and arrangement within DaVinci Resolve.

> :warning: The project's API design in Resolve is frustrating due to its poor design. Who writes such subpar APIs?

## Quick Start

### Using uv for Package Management

This project uses [uv](https://uv.python.com) as the package management tool. Please follow these steps to set up:

1. **Install uv**
    ```bash
    pip install uv
    ```

2. **Install Dependencies**
    ```bash
    uv sync
    ```

For more information on using uv, refer to the [uv documentation](https://uv.python.com/docs).

## Project Features

## Usage of main.py

`main.py` is the entry script of the project, used to import and organize audio files. You can specify the audio folder path and project name using command-line arguments.

**Command Format:**
```bash
uv run main.py --folder_path <audio folder path> --project_name <project name>
```

**Parameters:**
- `--folder_path`: Specifies the folder path containing time-coded audio files.
- `--project_name`: Specifies the project name to create in DaVinci Resolve.

**Example:**
```bash
uv run main.py --folder_path "D:\AudioFiles" --project_name "MyProject"
```

## Project Requirements

To ensure the project runs correctly, please prepare the following:

1. **Time-Coded Audio Files**: Ensure all WAV format audio files contain accurate timecode information for the script to correctly process and organize.
2. **Folder Structure**: Audio files should be categorized by character and track. For example:
    ```
    AudioFiles/
    ├── CharacterA/
    │   ├── Track1/
    │   │   ├── audio1.wav
    │   │   └── audio2.wav
    │   └── Track2/
    └── CharacterB/
        └── Track1/
            └── audio3.wav
    ```

**Notes:**
- Ensure the timecodes in the audio files are accurate.
- Avoid using special characters in folder and track names to prevent script parsing errors.
- All audio files should be in WAV format and located in the specified folder path.

## File Descriptions

- `main.py`: Project entry point, responsible for parsing command-line arguments and executing the import and organization of audio files.
- `item_creator.py`: Contains the function `add_wav_files_with_structure`, used to import WAV files into the media pool and encapsulate them as `DRMediaItem` objects.
- `item_arranger.py`: Responsible for grouping and rearranging media items based on characters and tracks, ensuring no timecode overlaps.
- `davinci_media_item.py`: Defines the `DRMediaItem` data class, representing media items in DaVinci Resolve, including timecode and file path information.
- `resolve_api_init.py`: Used to initialize and configure DaVinci Resolve's API interface.
- `.gitignore`: Git ignore file, specifying files and folders that should not be under version control.
- `.python-version`: Specifies the Python version used by the project.
- `pyproject.toml`: Project configuration file, defining project dependencies and metadata.
- `typings/DaVinciResolveScript.pyi`: Type definition file for the DaVinci Resolve API, assisting with type checking and autocompletion.
- `add_wav_file`, `__scratch_code__.py`: Auxiliary scripts and temporary code files used for development and testing.

# Acknowledgements

Thank you to [fusionscript-stubs](https://github.com/czukowski/fusionscript-stubs) for making scripting truly enjoyable. I love you, czukowski brother.

Thank you to [dftt-timecode](https://github.com/dftt/dftt-timecode) for simplifying many timecode operations. 