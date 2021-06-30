import os
import subprocess


from taskgraph import TaskGraph

from Executer import EXE_WRAPPER_NAME, BASH_FILE_NAME
from SimpleExecuter import SimpleExecuter
import multiprocessing


def run_activation_params(activation_params_list: []):

    run_python_path = os.path.abspath(BASH_FILE_NAME)
    exe_wrapper_path = os.path.abspath(EXE_WRAPPER_NAME)

    activation_params_list_str = ""
    for activation_params in activation_params_list:
        activationParams_str = SimpleExecuter.get_activation_parameters_str(activation_params)
        activation_params_list_str += f' "{activationParams_str}"'

    args_list = f'{run_python_path} {exe_wrapper_path} {activation_params_list_str}'

    subprocess.run(args_list, shell=True)

    print(args_list)


class TaskGraphExecuter(SimpleExecuter):
    task_graph: TaskGraph

    ids_to_tasks: {}

    def __init__(self):

        self.task_graph = TaskGraph(os.getcwd(), multiprocessing.cpu_count())
        self.ids_to_tasks = {}

    def _get_tasks_for_ids(self, exe_node_dependencies):

        ret_tasks_for_ids = None

        if exe_node_dependencies:
            ret_tasks_for_ids = []
            for dep in exe_node_dependencies:
                current_task = self.ids_to_tasks[dep]

                ret_tasks_for_ids.append(current_task)

        return ret_tasks_for_ids

    def execute(self, exe_node_name: str, activationParams_list: [],
                exe_node_dependencies: [] = None):

        tasks_for_ids = self._get_tasks_for_ids(exe_node_dependencies)

        task = self.task_graph.add_task(func=run_activation_params,
                                        args=[activationParams_list],
                                        dependent_task_list=tasks_for_ids,
                                        task_name=exe_node_name)

        self.ids_to_tasks[exe_node_name] = task

    def execute_task_graph(self):
        self.task_graph.close()
        self.task_graph.join()
