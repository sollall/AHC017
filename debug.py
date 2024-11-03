import logging
from omegaconf import OmegaConf

from utils.inout import run_module,parse_args,parse_unknown_args

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    args, unknown = parse_args()
    refine_unknown=parse_unknown_args(unknown)
    cfg_opt=OmegaConf.create(refine_unknown)

    run_module(args.module_name,cfg_opt,args.test_id)
