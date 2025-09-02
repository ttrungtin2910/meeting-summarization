"""
Base pipeline class to chain multiple modules together.
"""

import importlib
from typing import Any, Dict, List, Optional

import yaml

from .base_module import BaseModule

DEFAULT_MODULE_PATH = "ai_agent.application.services.modules"

class Pipeline:
    """
    Class for executing a sequence of modules in a pipeline.

    This class takes a list of modules, where each module transforms
    the input `state` and passes it to the next module.

    Attributes:
        modules (List[BaseModule]): List of modules to run sequentially.

    Methods:
        run(state: Dict[str, Any]) -> Dict[str, Any]:
            Executes all modules in order, passing and updating the state.
    """

    def __init__(self, modules: List[BaseModule]):
        """
        Initialize the pipeline with a list of modules.

        Args:
            modules (List[BaseModule]): A list of module instances
                that implement the BaseModule interface.
        """
        self.modules = modules

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the pipeline asynchronously by running each module in order.

        Each module receives the current state, processes it, and returns
        an updated state that is passed to the next module.

        Args:
            state (Dict[str, Any]): The initial state to pass through the pipeline.

        Returns:
            Dict[str, Any]: The final state after all modules have been executed.
        """
        for module in self.modules:
            state = await module.run(state)
        return state


def load_pipeline_from_yaml(yaml_path: str, init_args: Optional[Dict[str, Any]] = None) -> Pipeline:
    """
    Load a pipeline from a YAML file with support for injecting real objects.

    Args:
        yaml_path (str): Path to the YAML config file.
        init_args (Dict[str, Any], optional): Real objects to inject into modules.

    Returns:
        BasePipeline: The constructed pipeline.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    modules = []
    for module_config in config["modules"]:
        if "path" in module_config:
            module_path = module_config["path"]
        else:
            module_path = DEFAULT_MODULE_PATH
        class_name = module_config["class"]

        # Dynamic import
        module = importlib.import_module(module_path)
        module_class = getattr(module, class_name)

        # Instantiate
        if "init_args" in module_config:
            prepared_args = {}
            for arg_name, yaml_value in module_config["init_args"].items():
                # If yaml_value is a string and matches a key in real init_args, inject real object
                if init_args and isinstance(yaml_value, str) and yaml_value in init_args:
                    prepared_args[arg_name] = init_args[yaml_value]
                else:
                    prepared_args[arg_name] = yaml_value

            instance = module_class(**prepared_args)
        else:
            instance = module_class()

        modules.append(instance)

    return Pipeline(modules=modules)
