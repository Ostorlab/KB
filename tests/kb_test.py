"""KB json files test"""
import glob
import json
import pathlib
import pytest

from tests import conftest


def testJsonFiles_allFilesAreValid_testPasses():
    json_files = glob.glob("**/*.json", recursive=True)

    for json_file in json_files:
        with pathlib.Path(json_file).open(encoding="utf-8") as file:
            try:
                json_data = json.load(file)
                conftest.validate_json_format(json_data)
            except (ValueError, AssertionError) as e:
                pytest.fail(f"Validation failed for JSON file '{json_file}': {str(e)}")
