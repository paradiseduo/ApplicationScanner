import os
import importlib
import logging

from .. import ROOT_PATH, name

logger = logging.getLogger(__name__)

for item in os.listdir(os.path.join(ROOT_PATH, "Android")):
    if '__' in item or '.DS_Store' in item:
        continue
    else:
        prefix, suffix = os.path.splitext(item)
        if suffix == ".py":
            try:
                importlib.import_module(f"{name}.Android.{prefix}")
            except Exception as e:
                logger.exception(e)