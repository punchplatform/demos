#!/usr/bin/env python3
# -*- coding: utf-8 *-

import mlflow.pyfunc
import os
import numpy as np
import pandas as pd

from punchline_python.core.holders.input_holder import InputHolder
from punchline_python.core.holders.output_holder import OutputHolder
from punchline_python.core.node import AbstractNode


class PythonPrediction(AbstractNode):

    @AbstractNode.declare_string_param(name="model_uri", required=True, default="models:/{model}/{state}".format(model="timeseriesforecasting", state="production"))
    @AbstractNode.declare_string_param(name="decoration", required=True, default=["y"])
    @AbstractNode.declare_string_param(name="inputs", required=True, default=["y"])
    @AbstractNode.declare_string_param(name="project", required=True, default="ICS-R2020")
    @AbstractNode.declare_string_param(name="tool", required=True, default="jira")

    def __init__(self) -> None:
        super().__init__()
        # Decorators on this constructor are used by our job editor

    def execute(self, input_data: InputHolder, output_data: OutputHolder) -> None:
        print("Execute node")
        current_model_uri = self.settings['model_uri']
        current_inputs_column = self.settings['inputs']
        current_decorations_column = self.settings['decoration']
        current_project = self.settings['project']
        current_tool = self.settings['tool']

        current_input_data = input_data.get().toPandas()
        m, n = current_input_data.shape

        df_decorations = current_input_data[current_decorations_column].copy()
        df_inputs = current_input_data[current_inputs_column].copy()
        df_decorations["project"] = pd.Series([current_project for i in range(0, m)])
        df_decorations["tool"] = pd.Series([current_tool for i in range(0, m)])

        loaded_model = mlflow.pyfunc.load_model(current_model_uri)
        output_prediction = loaded_model.predict(df_inputs.to_numpy()).astype(int)

        result = pd.concat([df_decorations, df_inputs], axis=1)
        result['prediction'] = pd.Series(output_prediction)

        output_data.set(alias='data', value=result.iloc[-1:, :])
        print(result.iloc[-1:, :])


if __name__ == "__main__":
    print("main")
    os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'
    node = ComplexAlgorithm()
    input_data = InputHolder()
    sample_size = 10
    input_test = np.linspace(1, 25, sample_size)
    input_test = input_test.astype(int).reshape(sample_size, 1)
    df_input_test = pd.DataFrame(input_test)
    df_input_test.columns = ["y"]
    input_data.set(alias='data', value=df_input_test)
    output_data = OutputHolder()

    node.execute(input_data, output_data)
