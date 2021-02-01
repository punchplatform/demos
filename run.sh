#!/bin/bash

if [ -z "$PUNCH_DEMO_DIR" ] 
then
	echo "PUNCH_DEMO_DIR must be set"
	exit 1
else
	echo "$PUNCH_DEMO_DIR"
fi

if [ -z "$PUNCHPLATFORM_CONF_DIR" ] 
then
	echo "PUNCH_DEMO_DIR must be set"
	exit 1
else
	echo "$PUNCH_DEMO_DIR"
fi


echo "Installation in progress..."
echo "COPY TENANTS"
cp -r $PUNCH_DEMO_DIR/conf/tenants/* $PUNCHPLATFORM_CONF_DIR/tenants
echo "COPY KIBANA RESOURCES"
cp -r $PUNCH_DEMO_DIR/conf/resources/kibana/dashboards/* $PUNCHPLATFORM_CONF_DIR/resources/kibana/dashboards/
echo "COPY ES RESOURCES"
cp -r $PUNCH_DEMO_DIR/conf/resources/elasticsearch/* $PUNCHPLATFORM_CONF_DIR/resources/elasticsearch/
echo "COPY SPARK RESOURCES"
cp -r $PUNCH_DEMO_DIR/conf/resources/spark_custom_nodes/pyspark $PUNCHPLATFORM_CONF_DIR/resources/spark_custom_nodes/pyspark
echo "Import all Dashboards"
punchplatform-setup-kibana.sh --import
echo "Import ES templates"
punchplatform-push-es-templates.sh --directory $PUNCHPLATFORM_CONF_DIR/resources/elasticsearch/
echo "Build all pyspark nodes"
make -C $PUNCHPLATFORM_CONF_DIR/resources/spark_custom_nodes/pyspark all
echo "Copy pyspark nodes to your $PUNCHPLATFORM_BINARIES/extlib"
if [ ! -d $PUNCHPLATFORM_BINARIES/extlib/pyspark ]
then
	mkdir -p $PUNCHPLATFORM_BINARIES/extlib/pyspark
fi
cp $PUNCHPLATFORM_CONF_DIR/resources/spark_custom_nodes/pyspark/target/* $PUNCHPLATFORM_BINARIES/extlib/pyspark
echo "...Installation completed"
