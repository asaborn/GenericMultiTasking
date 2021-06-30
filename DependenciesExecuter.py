from typing import TypeVar, Generic, Any

TData = TypeVar('TData')


class TaskInfo(Generic[TData]):
    name: str
    group_name: str
    data: TData
    dependencies: []

    def __init__(self, task_name: str, group_name: str, task_data: TData, depends_list: []):
        self.name = task_name
        self.group_name = group_name
        self.data = task_data
        self.dependencies = depends_list


class TasksGroupInfo(Generic[TData]):
    group_name: str
    names: []
    data_list: []
    group_dependencies: set

    def __init__(self, group_name: str):
        self.group_name = group_name
        self.names = []
        self.data_list = []
        self.group_dependencies = set([])


class DependenciesExecuter(Generic[TData]):
    init_tasks_func: any
    end_tasks_func: any
    execute_tasks_func: any

    execution_queue = []

    task_name_to_info = {}

    def __init__(self, execute_tasks_func=None, init_tasks_func=None, end_tasks_func=None):
        self.init_tasks_func = init_tasks_func
        self.end_tasks_func = end_tasks_func
        self.execute_tasks_func = execute_tasks_func

    def _find_min_loc_for_task(self, depends_list):

        ret_index: int
        all_indexes = []

        if depends_list:
            for depended_task_name in depends_list:
                all_indexes.append(self.execution_queue.index(depended_task_name))

        if all_indexes:
            ret_index = max(all_indexes) + 1
        else:
            ret_index = len(self.execution_queue)

        return ret_index

    def add_exe_task(self, task_name: str, task_data: TData, depends_list: [] = None, group_name: str = None):
        if depends_list:
            updated_depends_list = []
            for depended in depends_list:
                if depended in self.task_name_to_info:
                    updated_depends_list.append(depended)
        else:
            updated_depends_list = None
        min_loc = self._find_min_loc_for_task(updated_depends_list)
        self.execution_queue.insert(min_loc, task_name)
        group_name_of_task = group_name
        depends_list_of_task = updated_depends_list
        if not group_name_of_task:
            group_name_of_task = task_name
        if not depends_list_of_task:
            depends_list_of_task = []

        self.task_name_to_info[task_name] = TaskInfo(task_name, group_name_of_task, task_data, depends_list_of_task)

    def get_number_of_groups_to_run(self):

        groups_set = set([])

        for task_name in self.execution_queue:
            task_info = self.task_name_to_info[task_name]

            group_name = task_info.group_name

            groups_set.add(group_name)

        return len(groups_set)

    def execute(self):

        if self.init_tasks_func:
            self.init_tasks_func()

        tasks_and_dependencies_per_group = {}

        for task_name in self.execution_queue:
            task_info = self.task_name_to_info[task_name]

            group_name = task_info.group_name

            if group_name not in tasks_and_dependencies_per_group.keys():
                tasks_and_dependencies_per_group[group_name] = TasksGroupInfo(group_name)

            tasks_and_dependencies_per_group[group_name].data_list.append(task_info.data)

            for task_dependency in task_info.dependencies:
                group_of_task_dep = self.task_name_to_info[task_dependency].group_name

                if group_of_task_dep != group_name:
                    tasks_and_dependencies_per_group[group_name].group_dependencies.add(group_of_task_dep)

        for group_name_data in tasks_and_dependencies_per_group.items():

            group_name, task_info = group_name_data

            data_list = task_info.data_list

            if len(task_info.group_dependencies) == 0:
                group_dependencies = None
            else:
                group_dependencies = list(task_info.group_dependencies)
                group_dependencies.sort()

            self.execute_tasks_func(group_name, data_list, group_dependencies)

        if self.end_tasks_func:
            self.end_tasks_func()

        self.execution_queue.clear()
