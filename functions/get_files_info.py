import os

def get_files_info(working_directory, directory=None):
    path = os.path.join(working_directory, directory)
    outside_working_dir = is_outside_working_dir(path)
    if outside_working_dir():
        f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(path) == False:
        f'Error: "{directory}" is not a directory'

def is_outside_working_dir(path):
    work_dir = os.path.abspath(os.getcwd())
    abs_path = os.path.abspath(path)
    common = os.path.commonpath([work_dir, abs_path])
    return common != work_dir

def is_dir(directory):

