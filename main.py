import os

from module_utility.ph import ph_source_extract
from module_utility.ph import ph_module_config

from module_utility.cl_1024 import cl_source_extract
from module_utility.cl_1024 import cl_module_config

def main():
    param_list = cl_module_config.load_config(os.path.join("config", "cl_1024", "config.json"), os.path.join("data", "cl_1024", "extract_data"))
    print(param_list)
    cl_source_extract.extract_link(param_list)
    
    param_list = ph_module_config.load_config(os.path.join("config", "ph", "config.json"), os.path.join("data", "ph", "extract_data"))
    ph_source_extract.extract_link(param_list)

main()
