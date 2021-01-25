#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from punchline_python.core.holders.input_holder import InputHolder
from punchline_python.core.holders.output_holder import OutputHolder
from punchline_python.core.node import AbstractNode

from pyspark.mllib.evaluation import MulticlassMetrics, BinaryClassificationMetrics
import datetime
import uuid
import json

class ComplexAlgorithm(AbstractNode):

    @AbstractNode.declare_param(name="prob_prediction_label", required=False, default="prediction")
    @AbstractNode.declare_param(name="expected_class_label", required=False, default="target")
    @AbstractNode.declare_param(name="model_type", required=False, default="Fishing")
    def __init__(self) -> None:
        super().__init__()

    def execute(self, input_data: InputHolder, output_data: OutputHolder) -> None:

        ds_final = {}
        ss = self.job_context.spark_session

        prob_prediction_label = self.settings["prob_prediction_label"]
        expected_class_label = self.settings["expected_class_label"]
        model_type = self.settings["model_type"]

        ds_prim = input_data.get(alias="predictions_data")

        # Normalize data
        ds_prim.createGlobalTempView("primitif")

        ds_gen_1 = ss.sql(
            "SELECT if( {prob_prediction_label} == '{model_type}', '1.0', '0.0') as prediction,  if( {expected_class_label} == '{model_type}', '1.0', '0.0') as expected "
            "FROM global_temp.primitif".format(prob_prediction_label=prob_prediction_label,
                                                expected_class_label=expected_class_label,
                                               model_type=model_type))

        ds_gen_2 = ds_gen_1.rdd.map(lambda a: (float(a.prediction), float(a.expected)))

        # Compute model performances metrics
        metricsMultiClass = MulticlassMetrics(ds_gen_2)
        metricsBinary = BinaryClassificationMetrics(ds_gen_2)
        label = 1.0

        ds_final["metrics"] = {}
        ds_final["metrics"]["AUC"] = metricsBinary.areaUnderROC
        ds_final["metrics"]["f_measure"] = metricsMultiClass.fMeasure(label, beta=1.0)
        ds_final["metrics"]["precision"] = metricsMultiClass.precision(label)
        ds_final["metrics"]["recall"] = metricsMultiClass.recall(label)
        ds_final["metrics"]["confusion_matrix"] = []

        confusion_matrix_values = metricsMultiClass.confusionMatrix().toArray()
        confusion_matrix_raw = {}
        confusion_matrix_raw["actual"] = "False"
        confusion_matrix_raw["predicted"] = "False"
        confusion_matrix_raw["value"] = confusion_matrix_values[0][0]
        ds_final["metrics"]["confusion_matrix"].append(confusion_matrix_raw)

        confusion_matrix_raw = {}
        confusion_matrix_raw["actual"] = "True"
        confusion_matrix_raw["predicted"] = "False"
        confusion_matrix_raw["value"] = confusion_matrix_values[0][1]
        ds_final["metrics"]["confusion_matrix"].append(confusion_matrix_raw)

        confusion_matrix_raw = {}
        confusion_matrix_raw["actual"] = "False"
        confusion_matrix_raw["predicted"] = "True"
        confusion_matrix_raw["value"] = confusion_matrix_values[1][0]
        ds_final["metrics"]["confusion_matrix"].append(confusion_matrix_raw)

        confusion_matrix_raw = {}
        confusion_matrix_raw["actual"] = "True"
        confusion_matrix_raw["predicted"] = "True"
        confusion_matrix_raw["value"] = confusion_matrix_values[1][1]
        ds_final["metrics"]["confusion_matrix"].append(confusion_matrix_raw)

        ds_final["metrics"]["boxplot_shiptype"] = {}
        ds_final["metrics"]["boxplot_other"] = {}

        ds_final["timestamp"] = str(datetime.datetime.now())
        ds_final["id"] = str(uuid.uuid1())

        ds_final = [{**ds_final}]

        output_data.set(ds_final)
