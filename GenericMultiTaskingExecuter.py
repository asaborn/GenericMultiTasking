import pandas as pd
import ast
import sys

from ActivationParams import ActivationParams
from DependenciesExecuter import DependenciesExecuter
from SlurmExecuter import SlurmExecuter
from SGEExecuter import SGEExecuter
from TaskGraphExecuter import TaskGraphExecuter


def get_dependencies_executer(multi_tasking_method: str):
    if multi_tasking_method == 'taskgraph':
        executer = TaskGraphExecuter()
        dep_executer = DependenciesExecuter[ActivationParams](execute_tasks_func=executer.execute,
                                                              end_tasks_func=executer.execute_task_graph)
    else:
        if multi_tasking_method == 'slurm':
            executer = SlurmExecuter()
        elif multi_tasking_method == 'sge':
            executer = SGEExecuter()
        else:
            raise ValueError("Wrong multi tasking method provided")

        dep_executer = DependenciesExecuter[ActivationParams](execute_tasks_func=executer.execute)

    return dep_executer


def main(args):

    multi_tasking_method = args[0]

    activation_params_scheme_csv_file_path = args[1]

    activation_params_scheme_df = pd.read_csv(activation_params_scheme_csv_file_path)

    dep_executer = get_dependencies_executer(multi_tasking_method)


    activation_params_scheme_df.fillna(0, inplace=True)
    activation_params_list = []
    for index, row in activation_params_scheme_df.iterrows():
        activation_params_dict = row.to_dict()

        check_input_files_before_run_string_list = activation_params_dict['CheckInputFilesBeforeRun']

        if check_input_files_before_run_string_list != 0:
            check_input_files_before_run = ast.literal_eval(
                check_input_files_before_run_string_list)
        else:
            check_input_files_before_run = None

        generated_files_string_list = activation_params_dict['GeneratedFiles']

        if generated_files_string_list != 0:
            generated_files = ast.literal_eval(
                generated_files_string_list)
        else:
            generated_files = None

        activation_params = ActivationParams(output_directory=activation_params_dict['OutputDirectory'],
                                             cmd_line=activation_params_dict['CmdLine'],
                                             binaries_location=activation_params_dict['BinariesLocation'],
                                             force=bool(activation_params_dict['Force']),
                                             stdout_file=activation_params_dict['StdoutFile'],
                                             stderr_file=activation_params_dict['StderrFile'],
                                             timeout_in_secs=int(activation_params_dict['TimeoutInSecs']),
                                             generated_files=generated_files,
                                             check_input_files_before_run=check_input_files_before_run,
                                             working_directory_to_binaries_dir=bool(
                                                 activation_params_dict['WorkingDirectoryToBinariesDir']),
                                             max_memory_usage=int(activation_params_dict['MaxMemoryUsage']),
                                             execution_time_file=activation_params_dict['ExecutionTimeFile'])

        activation_params_list.append(activation_params)

        dependencies_string_list = activation_params_dict['Dependencies']

        if dependencies_string_list != 0:
            dependencies = ast.literal_eval(
                dependencies_string_list)
        else:
            dependencies = None

        task_name = activation_params_dict['TaskName']
        group_name = activation_params_dict['GroupName']

        dep_executer.add_exe_task(task_name,
                                  activation_params, dependencies, group_name)

    dep_executer.execute()


if __name__ == '__main__':
    main(sys.argv[1:])
