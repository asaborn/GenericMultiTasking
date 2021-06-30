import os
import subprocess
import sys
from pathlib import PurePath
from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
import time

import ActivationParamsParser
import ActivationParams


def RunProcess(output_directory: str, binaries_location: str, cmd_line: str, is_redirect_stdout: bool,
               timeout_in_secs=None, working_directory_to_binaries_dir: bool = False,
               exe_time_file_path: str = None):
    stdout = None
    stderr = None
    if is_redirect_stdout:
        stdout = sys.stdout
        stderr = sys.stderr
    cmd_line_params_list = cmd_line.split()
    working_dir = binaries_location if working_directory_to_binaries_dir else output_directory
    if exe_time_file_path:
        start_time = time.time()
    try:
        completed_process = subprocess.run(cmd_line_params_list, cwd=working_dir, stdout=stdout, stderr=stderr,
                                           timeout=timeout_in_secs)
        return_code = completed_process.returncode
        if exe_time_file_path:
            time_elapsed = time.time() - start_time
    except subprocess.TimeoutExpired:
        print(f'Timeout expired after {timeout_in_secs} secs', file=sys.stderr)
        return_code = 1
        if exe_time_file_path:
            time_elapsed = 99999999
    if exe_time_file_path is not None:
        path_to_stdout_file = PurePath(exe_time_file_path)
        with open(path_to_stdout_file, 'w') as f_exe_time_file:
            f_exe_time_file.write(str(time_elapsed))
    if return_code != 0:
        print(f"Process '{cmd_line}' exited with error {return_code}", file=sys.stderr)
    return return_code


def PrepareOutputDirectory(force: bool, required_files=None, check_input_files_before_run=None,
                           current_files_paths_available=[]):
    generate_files = True
    input_files_not_exist = []

    if check_input_files_before_run:
        for input_file in check_input_files_before_run:
            if not (Path(input_file).is_file() | Path(input_file).is_dir()):
                input_files_not_exist.append(input_file)

    if input_files_not_exist:
        print(f'Required input files are missing: {" ".join(input_files_not_exist)} ', file=sys.stderr)
        generate_files = False
    else:

        if not force:
            if current_files_paths_available:
                all_files_exist = True
                current_index = 0

                if len(required_files) == len(current_files_paths_available):

                    while all_files_exist & (current_index < len(current_files_paths_available)):
                        current_file_path = current_files_paths_available[current_index]
                        all_files_exist = (os.stat(current_file_path.as_posix()).st_size != 0)
                        current_index += 1

                    generate_files = not all_files_exist

    return generate_files


def process_activation_params(activation_params: ActivationParams):
    ret_value = 0

    output_directory_path = Path(activation_params.output_directory)

    Path.mkdir(output_directory_path, parents=True, exist_ok=True)

    current_files_paths_available = []

    output_directory = activation_params.output_directory
    required_files = activation_params.generated_files
    # force = activation_params.force

    if required_files:
        for current_file in required_files:
            current_file_path = Path(output_directory, current_file)
            if current_file_path.is_file() | current_file_path.is_dir():
                current_files_paths_available.append(current_file_path)
                # if force:
                #    os.remove(current_file_path)

    stdout = sys.stdout
    stderr = sys.stderr

    f_stdout_file = None
    f_stderr_file = None

    if activation_params.stdout_file:
        path_to_stdout_file = PurePath(activation_params.stdout_file)
        f_stdout_file = open(path_to_stdout_file.as_posix(), "a+")
        stdout = f_stdout_file

    if activation_params.stderr_file:
        path_to_stderr_file = PurePath(activation_params.stderr_file)
        f_stderr_file = open(path_to_stderr_file.as_posix(), "a+")
        stderr = f_stderr_file

    with redirect_stdout(stdout), redirect_stderr(stderr):

        generate_files = PrepareOutputDirectory(activation_params.force,
                                                activation_params.generated_files,
                                                activation_params.check_input_files_before_run,
                                                current_files_paths_available)

        if generate_files:
            is_redirect_stdout = activation_params.stdout_file
            ret_value = RunProcess(activation_params.output_directory, activation_params.binaries_location,
                                   activation_params.cmd_line, is_redirect_stdout,
                                   activation_params.timeout_in_secs,
                                   activation_params.working_directory_to_binaries_dir,
                                   activation_params.execution_time_file)

    if f_stdout_file:
        f_stdout_file.close()
    if f_stderr_file:
        f_stderr_file.close()

    return ret_value


def main(args):
    ret_value = 0

    for activation_params_str in args:
        activation_params = ActivationParamsParser.ActivationParamsParser.parse_activation_parameters_str(
            activation_params_str)
        ret_value = process_activation_params(activation_params) | ret_value

    return ret_value


if __name__ == '__main__':
    exit_value = main(sys.argv[1:])
    exit(exit_value)
