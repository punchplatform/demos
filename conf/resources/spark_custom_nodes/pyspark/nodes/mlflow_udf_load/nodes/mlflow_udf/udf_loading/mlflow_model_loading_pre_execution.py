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
        model_uri = "models:/{model}/{state}".format(model=model_registry_id, state=model_registry_stage)
        # Test output expected type
        if(data_type == 'regression'):
            data_type = DoubleType()
        
        elif( (data_type == 'classification') or (data_type == 'clustering') ):
            data_type = StringType()
        
        mlflow.set_tracking_uri("http://{hostname}:{port}".format(hostname=mlflow_host, port=mlflow_port))

        # Generate a pandas UDF function
        prediction = mlflow.pyfunc.spark_udf(spark=self.__spark_session, model_uri=model_uri, result_type=data_type)
        self.__spark_session.udf.register("prediction", prediction)
