import os

from module_utility.ph import ph_source_extract
from module_utility.ph import module_config

def main():
    param_list = module_config.load_config(os.path.join("config", "ph", "config.json"), os.path.join("data", "ph", "extract_data"))
    ph_source_extract.extract_link(param_list)

main()

