from abc import ABC, abstractmethod

import ActivationParams
from ActivationParamsParser import ActivationParamsParser

BASH_FILE_NAME = 'run_python.sh'
EXE_WRAPPER_NAME = 'ExeWrapper.py'


class Executer(ABC):

    @abstractmethod
    def execute(self, exe_node_name, activationParams_list: [], exe_node_dependencies: [] = None):
        pass

    @staticmethod
    def get_activation_parameters_args(activation_params: ActivationParams):
        return ActivationParamsParser.get_activation_parameters_args(activation_params)

    @staticmethod
    def get_activation_parameters_str(activation_params: ActivationParams):
        return ActivationParamsParser.get_activation_parameters_str(activation_params)







