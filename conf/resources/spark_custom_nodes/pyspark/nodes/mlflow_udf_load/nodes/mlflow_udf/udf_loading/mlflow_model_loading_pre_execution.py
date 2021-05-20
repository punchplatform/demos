#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License Agreement
# This code is licensed under the outer restricted Tiss license:
#
#  Copyright [2014]-[2020] Thales Services under the Thales Inner Source Software License
#  (Version 1.0, InnerPublic -OuterRestricted the "License");
#
#  You may not use this file except in compliance with the License.
#
#  The complete license agreement can be requested at contact@punchplatform.com.
#
#  Refer to the License for the specific language governing permissions and limitations
#  under the License.

from pyspark.sql.types import StringType
from pyspark.sql.types import DoubleType
from pyspark.sql.session import SparkSession
from pyspark import SparkConf
import mlflow
import requests
import json

__author__ = "pierre"

class MlflowModelLoadingPreExecution(object):

    __spark_session: SparkSession
    
    def __init__(self) -> None:
        self.__spark_session = SparkSession.builder.getOrCreate()
        self.pre()

    def pre(self) -> None:
        data_type = SparkConf().get("spark.punch.mlflow.model.type")
        model_registry_id = SparkConf().get("spark.punch.mlflow.model.registry.id")
        model_registry_stage = SparkConf().get("spark.punch.mlflow.model.registry.stage")
        mlflow_host = SparkConf().get("spark.punch.mlflow.host")
        mlflow_port = SparkConf().get("spark.punch.mlflow.port")
        
        # Test output expected type
        if(data_type == 'regression'):
            data_type = DoubleType()
        
        elif( (data_type == 'classification') or (data_type == 'clustering') ):
            data_type = StringType()

        # Fetch the latest model version
        registry_uri = "http://{hostname}:{port}/api/2.0/preview/mlflow/registered-models/get".format(hostname=mlflow_host, port=mlflow_port)
        registry_params = {"name" : model_registry_id}
        result = requests.get(registry_uri, registry_params)
        payload = json.loads(result.text)
        model_latest = payload["registered_model"]["latest_versions"]
        model_to_return = None
        for model in model_latest:
            if(model['current_stage'].lower() == current_model_registry_stage.lower()):
                model_to_return = model
            else:
                pass
        # Generate a pandas UDF function
        prediction = mlflow.pyfunc.spark_udf(spark=self.__spark_session, model_uri=model_to_return, result_type=data_type)
        self.__spark_session.udf.register("prediction", prediction)
