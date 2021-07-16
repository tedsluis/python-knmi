import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

api_url = "https://api.dataplatform.knmi.nl/open-data"
api_version = "v1"


def main():
    # Parameters
    api_key = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6ImNjOWE2YjM3ZjVhODQwMDZiMWIzZGIzZDRjYzVjODFiIiwiaCI6Im11cm11cjEyOCJ9"
    dataset_name = "Actuele10mindataKNMIstations"
    dataset_version = "2"

    # Use get file to retrieve a file from one hour ago.
    # Filename format for this dataset equals KMDS__OPER_P___10M_OBS_L2_YYYYMMDDHHMM.nc,
    # where the minutes are increased in steps of 10.
    timestamp_now = datetime.utcnow()
    timestamp_one_hour_ago = (
        timestamp_now
        - timedelta(hours=1)
        - timedelta(minutes=timestamp_now.minute % 10)
    )
    filename = (
        f"KMDS__OPER_P___10M_OBS_L2_{timestamp_one_hour_ago.strftime('%Y%m%d%H%M')}.nc"
    )

    logger.info(f"Current time: {timestamp_now}")
    logger.info(f"One hour ago: {timestamp_one_hour_ago}")
    logger.info(f"Dataset file to download: {filename}")

    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})

    if get_file_response.status_code != 200:
        logger.error("Unable to retrieve download url for file")
        logger.error(get_file_response.text)
        sys.exit(1)

    logger.info(
        f"Successfully retrieved temporary download URL for dataset file {filename}"
    )

    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)

    # Write dataset file to disk
    p = Path(filename)
    p.write_bytes(dataset_file_response.content)

    logger.info(f"Successfully downloaded dataset file to {p}")

    # Check logging for deprecation
    if "X-KNMI-Deprecation" in get_file_response.headers:
        deprecation_message = get_file_response.headers.get("X-KNMI-Deprecation")
        logger.warning(f"Deprecation message: {deprecation_message}")


if __name__ == "__main__":
    main()
