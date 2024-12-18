# Davinci Resolve 自动导入脚本

 [ENGLISH README](./README_EN.md)

~~臣欲Track，陛下何故长眠~~

## 项目介绍

本项目旨在通过自动化脚本将带有时间码的音频文件（WAV格式）导入到 DaVinci Resolve 中，并按照预定的文件夹结构进行组织。主要功能包括：

1. **导入音频文件**：递归扫描指定文件夹中的WAV文件，并将其导入到DaVinci Resolve的媒体池中。
2. **组织媒体项**：根据音频文件的文件夹结构，自动分配角色和轨道，避免时间码重叠。
3. **时间码管理**：处理带有时间码的音频文件，确保在DaVinci Resolve中的正确同步和排列。

> :warning:本项目中道崩殂于Resolve的愚蠢API设计:innocent:谁家好人写API还缺一级的？

## 快速开始

### 使用 uv 进行包管理

本项目使用 [uv](https://uv.python.com) 作为包管理工具。请按照以下步骤进行设置：

1. **安装uv**
    ```bash
    pip install uv
    ```

2. **安装依赖**
    ```bash
    uv sync
    ```

更多关于 uv 的使用，请参考 [uv 文档](https://uv.python.com/docs)。

## 项目功能

## main.py 的用法

`main.py` 是项目的入口脚本，用于执行音频文件的导入和组织。使用命令行参数可以指定音频文件夹路径和项目名称。

**命令格式：**
```bash
uv run main.py --folder_path <音频文件夹路径> --project_name <项目名称>
```

**参数说明：**
- `--folder_path`：指定包含带时间码的音频文件的文件夹路径。
- `--project_name`：指定在DaVinci Resolve中创建的项目名称。

**示例：**
```bash
uv run main.py --folder_path "D:\AudioFiles" --project_name "MyProject"
```

## 项目准备材料

为确保项目正常运行，请准备以下材料：

1. **带时间码的音频文件**：确保所有WAV格式的音频文件中包含准确的时间码信息，以便脚本正确处理和组织。
2. **文件夹结构**：音频文件应按照角色和轨道进行分类存放。例如：
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

**注意事项：**
- 确保音频文件的时间码准确无误。
- 避免文件夹和轨道名称中包含特殊字符，以防止脚本解析错误。
- 所有音频文件应为WAV格式，并位于指定的文件夹路径下。

## 各文件说明

- `main.py`：项目入口，负责解析命令行参数并执行音频文件的导入和组织。
- `item_creator.py`：包含函数 `add_wav_files_with_structure`，用于将WAV文件导入媒体池并封装为 `DRMediaItem` 对象。
- `item_arranger.py`：负责根据角色和轨道对媒体项进行分组和重新排列，确保时间码不重叠。
- `davinci_media_item.py`：定义 `DRMediaItem` 数据类，用于表示DaVinci Resolve中的媒体项，包括时间码和文件路径信息。
- `resolve_api_init.py`：用于初始化和配置DaVinci Resolve的API接口。
- `.gitignore`：Git忽略文件，指定不需要纳入版本控制的文件和文件夹。
- `.python-version`：指定项目使用的Python版本。
- `pyproject.toml`：项目配置文件，定义项目依赖和元数据。
- `typings/DaVinciResolveScript.pyi`：DaVinci Resolve API的类型定义文件，辅助类型检查和自动补全。
- `add_wav_file`、`__scratch_code__.py`：辅助脚本和临时代码文件，用于开发和测试。

# 致谢

感谢[fusionscript-stubs](https://github.com/czukowski/fusionscript-stubs)，让我真的Happy scripting，我爱你，czukowski老哥。

感谢[dftt-timecode](https://github.com/dftt/dftt-timecode)，它简化了很多时间码的操作。