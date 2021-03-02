#!/usr/bin/env python3
# -*- coding: utf-8 *-

import mlflow.pyfunc
import mlflow
import os
import numpy as np
import pandas as pd
import requests
import json

from punchline_python.core.holders.input_holder import InputHolder
from punchline_python.core.holders.output_holder import OutputHolder
from punchline_python.core.node import AbstractNode


class PythonPrediction(AbstractNode):

    @AbstractNode.declare_string_param(name="model_registry_id", required=True, default="ICS-R2020-SE_jiratcm")
    @AbstractNode.declare_string_param(name="model_registry_stage", required=True, default="production")
    @AbstractNode.declare_string_param(name="decoration", required=True, default=["y"])
    @AbstractNode.declare_string_param(name="inputs", required=True, default=["y"])
    @AbstractNode.declare_string_param(name="mlflow_host", required=True, default="localhost")
    @AbstractNode.declare_string_param(name="mlflow_port", required=True, default="5000")

    def __init__(self) -> None:
        super().__init__()
        # Decorators on this constructor are used by our job editor

    def execute(self, input_data: InputHolder, output_data: OutputHolder) -> None:
        current_model_registry_id = self.settings['model_registry_id']
        current_model_registry_stage = self.settings['model_registry_stage']
        current_model_uri = "models:/{model}/{state}".format(model=current_model_registry_id, state=current_model_registry_stage)
        current_inputs_column = self.settings['inputs']
        current_decorations_column = self.settings['decoration']
        current_mlflow_host = self.settings['mlflow_host']
        current_mlflow_port = self.settings['mlflow_port']

        current_input_data = input_data.get().toPandas()
        m, n = current_input_data.shape

        mlflow.set_tracking_uri("http://{hostname}:{port}".format(hostname=current_mlflow_host, port=current_mlflow_port))
        df_decorations = current_input_data[current_decorations_column].copy()
        df_inputs = current_input_data[current_inputs_column].copy()

        loaded_model = mlflow.pyfunc.load_model(current_model_uri)
        output_prediction = loaded_model.predict(df_inputs.to_numpy()).astype(int)


        current_registry_uri = "http://{hostname}:{port}/api/2.0/preview/mlflow/registered-models/get".format(hostname=current_mlflow_host, port=current_mlflow_port)
        current_registry_params = {"name" : current_model_registry_id}
        result = requests.get(current_registry_uri, current_registry_params)
        payload = json.loads(result.text)
        model_latest = payload["registered_model"]["latest_versions"]
        model_to_return = None
        for model in model_latest:
            if(model['current_stage'].lower() == current_model_registry_stage.lower()):
                model_to_return = model
            else:
                pass
    
        df_meta_data = pd.DataFrame([{"meta" : model_to_return} for i in range(0, m)])

        result = pd.concat([df_decorations, df_inputs, df_meta_data], axis=1)
        result['prediction'] = pd.Series(output_prediction)

        output_data.set(alias='data', value=result.iloc[-1:, :])


