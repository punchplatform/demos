from optparse import OptionParser

from project.generator.GeneratorFactory import GeneratorFactory
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

for payload in configuration["use_case"]:
    output_file_path = configuration["use_case"][payload]["output_logs"]
    class_name = configuration["use_case"][payload]["class"]
    module_name = configuration["use_case"][payload]["module"]
    generator = GeneratorFactory.GeneratorBuild(module_name, class_name)
    generator.generateDataset(
        configuration["use_case"][payload]["payload"], output_file_path
    )
exit(0)
