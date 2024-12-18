from item_creator import add_wav_files_with_structure
from resolve_api_init import RESOLVE


import click

@click.command()
@click.option(
    '--folder_path',
    help='文件夹路径'
)
@click.option(
    '--project_name',
    help='项目名称'
)
def main(folder_path: str, project_name: str):
    project = RESOLVE.GetProjectManager().CreateProject(project_name)
    if project is None:
        print("输入的项目名称不唯一，请尝试另一个")
        return
    pool = project.GetMediaPool()
    return add_wav_files_with_structure(pool, folder_path)


if __name__ == "__main__":
    main()

