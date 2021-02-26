help:
	@echo "all                  - Build all subprojects and regroup them in a common directory"

build: 
	@$(MAKE) -C nodes/mlflow_udf_load package name="mlflow_udf.pex"
	@$(MAKE) -C nodes/python_mlflow_prediction_node package name="python_mlflow_prediction.pex"

prepare: 
	@ mkdir ./target & cp ./nodes/*/dist/*.pex ./target

all: build prepare
