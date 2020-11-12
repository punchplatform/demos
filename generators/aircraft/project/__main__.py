from optparse import OptionParser

from project.utils.Utils import (
    generate_linear_aircraft_sensor_values,
    write_array_json_to_file,
)
from project.utils.Configuration import Configuration

parser = OptionParser()
parser.add_option(
    "-c",
    "--configuration",
    action="store",
    type="string",
    dest="configuration",
    help="Path to the Configuration file",
)

(options, args) = parser.parse_args()

if not options.configuration:
    parser.error("options -c is mandatory")

Configuration.setUp(options.configuration)
configuration = Configuration.getConfiguration().getConf()

# Aircraft Use Case
output_file_path = configuration["use_case"]["aircraft"]["output_logs"]
for conf in configuration["use_case"]["aircraft"]["payload"]:
    data = generate_linear_aircraft_sensor_values(**conf)
    write_array_json_to_file(data, output_file_path)
