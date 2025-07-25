import logging
import os

log_dir = os.path.expanduser('~/FOOTBALL_APP/logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=f'{log_dir}/predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log_prediction(match_info, prediction):
    logging.info(f"{match_info}: {prediction}")
