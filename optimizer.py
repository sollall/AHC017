from concurrent.futures import ProcessPoolExecutor
import logging
import hydra
from omegaconf import DictConfig

from utils.inout import run_module

logging.basicConfig(level=logging.INFO)

@hydra.main(config_path='./conf', config_name='config', version_base="1.3")
def main(cfg:DictConfig):

    if cfg.general.executor_type=="ProcessPoolExecutor":
        executor_class=ProcessPoolExecutor
    else:
        raise ValueError("Please specify the executor type.")

    total_score,total_time=0,0
    with executor_class(max_workers=cfg.general.max_workers) as executor:
        results = executor.map(run_module,
                                [cfg.general.module_name for _ in range(cfg.general.num_tests)],
                                [cfg.optimizer for _ in range(cfg.general.num_tests)],
                                [i for i in range(cfg.general.num_tests)]
                            )
        for result in results:
            score,passed_time=result
            total_score+=score
            total_time+=passed_time

    logging.info(f"{total_score},{passed_time}")
    return total_score

if __name__ == "__main__":
    main()