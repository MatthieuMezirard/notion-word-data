# Third party imports
import pytest
import requests

# Custom imports
from notion_word_data import word_data
from notion_word_data import errors


def test_check_language_success() -> None:
    word_data.WordData.check_language("en")


def test_check_language_failure_InvalidLanguage() -> None:
    with pytest.raises(errors.InvalidLanguage):
        word_data.WordData.check_language("invalid")


def test_fetch_word_data_success() -> None:
    test = word_data.WordData("test", "en", requests.Session())
    assert test.data == {
        "Test": {
            "Noun": {
                "A procedure intended to establish the quality, performance, or reliability of something, especially before it is taken into widespread use.": [
                    ["”Both countries carried out nuclear tests in may”"],
                    [
                        "Trial",
                        "Experiment",
                        "Try-out",
                        "Check",
                        "Examination",
                        "Assessment",
                        "Evaluation",
                        "Appraisal",
                        "Investigation",
                        "Inspection",
                        "Analysis",
                        "Scrutiny",
                        "Study",
                        "Probe",
                        "Exploration",
                        "Screening",
                        "Audition",
                        "Screen test",
                        "Assay",
                    ],
                ],
                "Short for test match.": [["”The first test against new zealand”"], []],
            },
            "Verb": {
                "Take measures to check the quality, performance, or reliability of (something), especially before putting it into widespread use or practice.": [
                    ["”This range has not been tested on animals”"],
                    [
                        "Try out",
                        "Trial",
                        "Pilot",
                        "Check",
                        "Examine",
                        "Assess",
                        "Evaluate",
                        "Appraise",
                        "Investigate",
                        "Analyse",
                        "Scrutinize",
                        "Study",
                        "Probe",
                        "Explore",
                        "Sample",
                        "Screen",
                        "Assay",
                    ],
                ]
            },
        }
    }


def test_fetch_word_data_failure_InvalidWord() -> None:
    with pytest.raises(errors.InvalidWord):
        word_data.WordData("wogewpvgfa", "en", requests.Session())
