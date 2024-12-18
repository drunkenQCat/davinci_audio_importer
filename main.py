from item_creator import add_wav_files_with_structure
from resolve_api_init import RESOLVE


def main(folder_path: str, project_name: str = "test"):
    project = RESOLVE.GetProjectManager().CreateProject(project_name)
    if project is None:
        print("The input Project Name is not unique, try another")
        return
    pool = project.GetMediaPool()
    return add_wav_files_with_structure(pool, folder_path)


if __name__ == "__main__":
    main(r"C:\CreativeProjects\Project\Audio Files\OrganizedFiles")
