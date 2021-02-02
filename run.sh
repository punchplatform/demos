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
	echo "PUNCHPLATFORM_CONF_DIR"
	exit 1
else
	echo "$PUNCHPLATFORM_CONF_DIR"
fi

if [ -z "$PUNCHPLATFORM_BINARIES_DIR" ] 
then
	echo "PUNCHPLATFORM_BINARIES_DIR must be set"
	exit 1
else
	echo "$PUNCHPLATFORM_BINARIES_DIR"
fi

echo "Installation in progress..."
echo "COPY TENANTS"
cp -r $PUNCH_DEMO_DIR/conf/tenants/* $PUNCHPLATFORM_CONF_DIR/tenants
echo "COPY KIBANA RESOURCES"
cp -r $PUNCH_DEMO_DIR/conf/resources/kibana/dashboards/* $PUNCHPLATFORM_CONF_DIR/resources/kibana/dashboards/
echo "COPY ES RESOURCES"
cp -r $PUNCH_DEMO_DIR/conf/resources/elasticsearch/* $PUNCHPLATFORM_CONF_DIR/resources/elasticsearch/
echo "COPY PYSPARK NODES"
cp -r $PUNCH_DEMO_DIR/conf/resources/spark_custom_nodes/pyspark $PUNCHPLATFORM_CONF_DIR/resources/spark_custom_nodes
echo "BUILD ALL PYSPARK NODES"
make -C $PUNCHPLATFORM_CONF_DIR/resources/spark_custom_nodes/pyspark all
echo "COPY PYSPARK NODES TO YOUR $PUNCHPLATFORM_BINARIES_DIR/extlib"
if [ ! -d $PUNCHPLATFORM_BINARIES_DIR/extlib/pyspark ]
then
	mkdir -p $PUNCHPLATFORM_BINARIES_DIR/extlib/pyspark
fi
cp $PUNCHPLATFORM_CONF_DIR/resources/spark_custom_nodes/pyspark/target/* $PUNCHPLATFORM_BINARIES_DIR/extlib/pyspark
echo "IMPORT ALL DASHBOARDS"
punchplatform-setup-kibana.sh --import
echo "IMPORT ES TEMPLATES"
punchplatform-push-es-templates.sh --directory $PUNCHPLATFORM_CONF_DIR/resources/elasticsearch/
echo "BUILD PYTHON GENERATORS PROJECT"
make package -C $PUNCH_DEMO_DIR/generators/tool name=tool
echo "CREATE /data REPO"
if [ ! -d /data ]
then
	mkdir /data
fi
echo "CREATE DATASETS"
python $PUNCH_DEMO_DIR/generators/tool/dist/tool.pex -c $PUNCH_DEMO_DIR/generators/tool/config/config.json
echo "PUSH SOME MANDATORY DATA INTO ES"
curl -H "Content-type: application/json" --data-binary @$PUNCH_DEMO_DIR/data/world_map.json -XPOST http://localhost:9200/world-map-import/_bulk?pretty
echo "...Installation completed"
