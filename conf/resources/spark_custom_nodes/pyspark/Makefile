help:
	@echo "all                  - Build all subprojects and regroup them in a common directory"

build: 
	@$(MAKE) -C nodes/mlflow_udf_load package name="mlflow_udf.pex"

prepare: 
	@ cp ./nodes/*/dist/*.pex ./target

all: build prepare
