class ActivationParams:
    output_directory: str
    cmd_line: str
    binaries_location: str
    force: bool
    stdout_file: str
    stderr_file: str
    timeout_in_secs: int
    generated_files: []
    check_input_files_before_run: []
    working_directory_to_binaries_dir: bool
    max_memory_usage: int
    execution_time_file: str

    def __init__(self, output_directory: str, cmd_line: str, binaries_location: str = None, force: bool = None, stdout_file: str = None,
                 stderr_file: str = None, timeout_in_secs: int = None, generated_files: [] = None , check_input_files_before_run: [] = None,
                 working_directory_to_binaries_dir: bool = None, max_memory_usage: int = None, execution_time_file: str = None):
        self.output_directory = output_directory
        self.cmd_line = cmd_line
        self.binaries_location = binaries_location
        self.force = force
        self.stdout_file = stdout_file
        self.stderr_file = stderr_file
        self.timeout_in_secs = timeout_in_secs
        self.generated_files = generated_files
        self.check_input_files_before_run = check_input_files_before_run
        self.working_directory_to_binaries_dir = working_directory_to_binaries_dir
        self.max_memory_usage = max_memory_usage
        self.execution_time_file = execution_time_file

    def __eq__(self, other):
        is_equal = (self.output_directory == other.output_directory) & \
                   (self.cmd_line == other.cmd_line) & \
                   (self.binaries_location == other.binaries_location) & \
                   (self.force == other.force) & \
                   (self.stdout_file == other.stdout_file) & \
                   (self.stderr_file == other.stderr_file) & \
                   (self.timeout_in_secs == other.timeout_in_secs) & \
                   (self.generated_files == other.generated_files) & \
                   (self.check_input_files_before_run == other.check_input_files_before_run) & \
                   (self.working_directory_to_binaries_dir == other.working_directory_to_binaries_dir) & \
                   (self.max_memory_usage == other.max_memory_usage) & \
                   (self.execution_time_file == other.execution_time_file)

        return is_equal
