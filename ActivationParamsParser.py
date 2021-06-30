import argparse

import ActivationParams


class ActivationParamsParser:
    parser = argparse.ArgumentParser('ExeWrapper')

    parser.add_argument('-outputDirectory', '--outputDirectoryValue', type=str, required=True)
    parser.add_argument('-binariesLocation', '--binariesLocationValue', type=str,
                        required=False)
    parser.add_argument('-workingDirectoryToBinariesDir', action='store_true')
    parser.add_argument('-cmdLine', type=str, required=True)
    parser.add_argument('-force', action='store_true')
    parser.add_argument('-stdoutFile', '--stdoutFileValue', type=str, required=False)
    parser.add_argument("-stderrFile", '--stderrFileValue', type=str, required=False)
    parser.add_argument("-timeout", "--timeoutValue", type=int, required=False)
    parser.add_argument('-generatedFiles', nargs='+', required=False)
    parser.add_argument('-checkInputFilesBeforeRun', nargs='+', required=False)
    parser.add_argument('-maxMemoryUsage', '--maxMemoryUsageValue', type=int, required=False)
    parser.add_argument("-executionTimeFile", '--executionTimeFileValue', type=str, required=False)

    @staticmethod
    def parse_activation_parameters(args=None):

        parser = ActivationParamsParser.parser

        args_parsed = parser.parse_args(args)

        output_directory = args_parsed.outputDirectoryValue

        cmd_line = args_parsed.cmdLine

        binaries_location = args_parsed.binariesLocationValue

        force = args_parsed.force

        stdout_file = args_parsed.stdoutFileValue
        stderr_file = args_parsed.stderrFileValue

        timeout_in_secs = args_parsed.timeoutValue

        generated_files = args_parsed.generatedFiles

        check_input_files_before_run = args_parsed.checkInputFilesBeforeRun

        working_directory_to_binaries_dir = args_parsed.workingDirectoryToBinariesDir

        max_memory_usage = 1

        if args_parsed.maxMemoryUsageValue:
            max_memory_usage = args_parsed.maxMemoryUsageValue

        execution_time_file = args_parsed.executionTimeFileValue

        activation_params = ActivationParams.ActivationParams(output_directory, cmd_line, binaries_location, force,
                                                              stdout_file, stderr_file, timeout_in_secs,
                                                              generated_files, check_input_files_before_run,
                                                              working_directory_to_binaries_dir, max_memory_usage,
                                                              execution_time_file)

        return activation_params

    @staticmethod
    def parse_activation_parameters_str(args_str: str):

        args = ActivationParamsParser.build_activation_parameters_args(args_str)
        ret_activation_params = ActivationParamsParser.parse_activation_parameters(args)

        return ret_activation_params

    @staticmethod
    def get_activation_parameters_str(activationParams: ActivationParams.ActivationParams):

        ret_str = f'-outputDirectory {activationParams.output_directory}'

        if activationParams.binaries_location:
            ret_str += f' -binariesLocation {activationParams.binaries_location}'
        if activationParams.working_directory_to_binaries_dir:
            ret_str += f' -workingDirectoryToBinariesDir'
        if activationParams.force:
            ret_str += f' -force'
        if activationParams.stdout_file:
            ret_str += f' -stdoutFile {activationParams.stdout_file}'
        if activationParams.stderr_file:
            ret_str += f' -stderrFile {activationParams.stderr_file}'
        if activationParams.timeout_in_secs:
            ret_str += f' -timeout {activationParams.timeout_in_secs}'
        if activationParams.generated_files:
            ret_str += f' -generatedFiles {" ".join(activationParams.generated_files)}'
        if activationParams.check_input_files_before_run:
            ret_str += f' -checkInputFilesBeforeRun {" ".join(activationParams.check_input_files_before_run)}'
        if activationParams.max_memory_usage:
            ret_str += f' -maxMemoryUsage {activationParams.max_memory_usage}'
        if activationParams.execution_time_file:
            ret_str += f' -executionTimeFile {activationParams.execution_time_file}'

        ret_str += f" -cmdLine '{activationParams.cmd_line}'"

        return ret_str

    @staticmethod
    def get_activation_parameters_args(activationParams: ActivationParams.ActivationParams):

        activation_params_str = ActivationParamsParser.get_activation_parameters_str(activationParams)

        args_list = ActivationParamsParser.build_activation_parameters_args(activation_params_str)

        return args_list

    @staticmethod
    def build_activation_parameters_args(activation_params_str: str):

        params_run_cmd_args_list = activation_params_str.split("'")

        args_list = params_run_cmd_args_list[0].split() + [params_run_cmd_args_list[1]]

        return args_list
