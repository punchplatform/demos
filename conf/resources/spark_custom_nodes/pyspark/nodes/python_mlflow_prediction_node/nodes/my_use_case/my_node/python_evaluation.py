#!/usr/bin/env python3
# -*- coding: utf-8 *-

import numpy as np
import pandas as pd
import importlib
import datetime

from punchline_python.core.holders.input_holder import InputHolder
from punchline_python.core.holders.output_holder import OutputHolder
from punchline_python.core.node import AbstractNode


class PythonEvaluation(AbstractNode):

    @AbstractNode.declare_string_param(name="evaluation_python_modules", required=True, default=["sklearn.metrics"])
    @AbstractNode.declare_string_param(name="evaluation_python_class", required=True, default=["mean_absolute_error"])
    @AbstractNode.declare_string_param(name="dataset_predicted_target_column", required=True, default=["y_pred"])
    @AbstractNode.declare_string_param(name="dataset_real_target_column", required=True, default=["y_real"])
    @AbstractNode.declare_string_param(name="dataset_decoration_column", required=True, default=["meta"])

    def __init__(self) -> None:
        super().__init__()
        # Decorators on this constructor are used by our job editor

    def execute(self, input_data: InputHolder, output_data: OutputHolder) -> None:
        #Load all settings
        current_predicted_target_column = self.settings['dataset_predicted_target_column']
        current_real_target_column = self.settings['dataset_real_target_column']
        current_python_modules = self.settings['evaluation_python_modules']
        current_python_class = self.settings['evaluation_python_class']
        current_decorations_columns = self.settings['dataset_decoration_column']

        current_input_data = input_data.get().toPandas()
        current_decoration = current_input_data.copy().loc[0, current_decorations_columns].tolist()
        output = []

        #Import classes
        for module, class_name in zip(current_python_modules, current_python_class):
            current_evaluation_obj = getattr(importlib.import_module(module), class_name)
            #Perform Evaluation
            current_evaluation_result = current_evaluation_obj(current_input_data[current_real_target_column], current_input_data[current_predicted_target_column])
            current_record = {'metric' : 
                                {'class' : class_name, 
                                'modules' : module, 
                                'score' : current_evaluation_result
                                },
                            'event_timestamp' : datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
                            }
            output.append(current_record)

        df_output = pd.DataFrame(output)
        m, n = df_output.shape 
        meta_data = [current_decoration for _ in range(0, m)]
        serie_meta_data = pd.DataFrame(meta_data)
        serie_meta_data.columns = current_decorations_columns
        df_output = pd.concat([df_output, serie_meta_data], axis=1)

        output_data.set(alias='data', value=df_output)
