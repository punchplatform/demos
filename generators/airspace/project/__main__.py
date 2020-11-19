from optparse import OptionParser

from project.utils.Utils import write_array_json_to_file, generate_random_shape_points, generate_random_radar_plots
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

# Airspace Use Case
output_file_path = configuration["use_case"]["airspace"]["output_logs"]
for conf in configuration["use_case"]["airspace"]["payload"]:
    data = generate_random_shape_points(**conf)
    write_array_json_to_file(data, output_file_path)

# radar Use Case
output_file_path = configuration["use_case"]["radar"]["output_logs"]
for conf in configuration["use_case"]["radar"]["payload"]:
    data = generate_random_radar_plots(**conf)
    write_array_json_to_file(data, output_file_path)