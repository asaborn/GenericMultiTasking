import os
import pathlib
import subprocess
import time

from ActivationParamsParser import ActivationParamsParser
from ActivationParams import ActivationParams
from Executer import Executer, EXE_WRAPPER_NAME


class SlurmExecuter(Executer):
    next_queue_index = 0
    
    def _get_max_mem_usage(self, activation_params_list: []):

        max_mem_value = 0

        for current_activation_param in activation_params_list:

            if current_activation_param.max_memory_usage > max_mem_value:
                max_mem_value = current_activation_param.max_memory_usage
            current_activation_param.max_memory_usage = None
        return max_mem_value

    def _execute_single_activation_params(self, exe_node_name: str, activation_params: ActivationParams,
                                          exe_node_dependencies: [] = None):
        working_directory = activation_params.binaries_location if activation_params.working_directory_to_binaries_dir \
            else activation_params.output_directory

        activation_params_for_sge = ActivationParams(activation_params.output_directory, activation_params.cmd_line,
                                                     None, activation_params.force,
                                                     None, None, activation_params.timeout_in_secs,
                                                     activation_params.generated_files,
                                                     activation_params.check_input_files_before_run, None, None)

        activation_params_for_sge_str = ActivationParamsParser.get_activation_parameters_str(activation_params_for_sge)

        dependencies, run_python_path, exe_wrapper_path = self._get_job_common_parameters(
            exe_node_dependencies)

        qsub_str = f'sbatch --job-name={exe_node_name} --chdir={working_directory} --mem={activation_params.max_memory_usage}G' \
            f' --output={activation_params.stdout_file} --error={activation_params.stderr_file}'

        params_run_cmd_args_list = qsub_str.split()

        if dependencies:
            params_run_cmd_args_list += dependencies

        params_run_cmd_args_list += [run_python_path, exe_wrapper_path]


        cmd_args_str = " ".join(params_run_cmd_args_list) + f' \"{activation_params_for_sge_str}\"'

        subprocess.run(cmd_args_str, shell=True)

    def _get_job_common_parameters(self, exe_node_dependencies: [] = None):

        dependencies = []

        if exe_node_dependencies:
            for dependency in exe_node_dependencies:
                #dependencies.append(f'--dependency=$(sacct -n -X --format jobid --name {dependency} | tail -1)')
                dependencies.append(f'--dependency=$(squeue --noheader --format %i --name {dependency})')
        run_python_path = os.path.abspath('sbatch_cpu.sh')
        exe_wrapper_path = os.path.abspath(EXE_WRAPPER_NAME)

        return dependencies, run_python_path, exe_wrapper_path

    def execute(self, exe_node_name: str, activation_params_list: [], exe_node_dependencies: [] = None):
        if (len(activation_params_list) == 1):
            self._execute_single_activation_params(exe_node_name, activation_params_list[0], exe_node_dependencies)

        else:

            dependencies, run_python_path, exe_wrapper_path = self._get_job_common_parameters(
                exe_node_dependencies)

            ts = time.time()

            stdout_file = f'{exe_node_name}_OUT_{ts}.o'
            stderr_file = f'{exe_node_name}_ERR_{ts}.e'

            output_directory = activation_params_list[0].output_directory

            if output_directory:

                stdout_file_path = pathlib.Path(output_directory, stdout_file).as_posix()

                stdout_err_file_path = pathlib.Path(output_directory, stderr_file).as_posix()
            else:

                stdout_file_path = pathlib.Path(activation_params_list[0].binaries_location, stdout_file).as_posix()
                stdout_err_file_path = pathlib.Path(activation_params_list[0].binaries_location, stderr_file).as_posix()

            max_mem_usage = self._get_max_mem_usage(activation_params_list)
            
            qsub_str = f'sbatch --job-name={exe_node_name} --mem={max_mem_usage}G' \
                f' --output={stdout_file_path} --error={stdout_err_file_path}'

            params_run_cmd_args_list = qsub_str.split()

            if dependencies:

                params_run_cmd_args_list += dependencies

            params_run_cmd_args_list += [run_python_path, exe_wrapper_path]

            application_params_strings = [f'\"{ActivationParamsParser.get_activation_parameters_str(activation_param)}\"'  
                                          for activation_param in activation_params_list]

            cmd_args_str = " ".join(params_run_cmd_args_list) + " " + " ".join(application_params_strings)

            subprocess.run(cmd_args_str, shell=True)

