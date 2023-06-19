"""KB json files test"""
import glob
import json
import pathlib

import pytest


def testJsonFiles_allFilesAreValid_testPasses() -> None:
    json_files = glob.glob("**/*.json", recursive=True)

    for json_file in json_files:
        with pathlib.Path(json_file).open(encoding="utf-8") as file:
            try:
                json_data = json.load(file)
            except ValueError as e:
                pytest.fail(f"Failed to load JSON file '{json_file}': {str(e)}")

            # Check if the JSON data is a dictionary
            assert isinstance(json_data, dict), "JSON data must be a dictionary."

            # Check if the required keys are present
            required_keys = ["risk_rating", "short_description", "references", "title"]
            for key in required_keys:
                assert (
                    key in json_data
                ), f"Required key '{key}' is missing in JSON data."

            # Check the data types and formats of the keys
            assert isinstance(
                json_data["risk_rating"], str
            ), "risk_rating must be a string."
            assert isinstance(
                json_data["short_description"], str
            ), "short_description must be a string."
            assert isinstance(
                json_data["references"], dict
            ), "references must be a dictionary."
            assert isinstance(json_data["title"], str), "title must be a string."

            # Check the format of the references
            references = json_data["references"]
            assert isinstance(references, dict), "references must be a dictionary."
