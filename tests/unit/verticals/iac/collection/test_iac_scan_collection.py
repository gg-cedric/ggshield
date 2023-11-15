import pytest

from ggshield.verticals.iac.collection.iac_scan_collection import (
    CollectionType,
    IaCScanCollection,
)
from tests.unit.verticals.iac.utils import (
    generate_diff_scan_collection,
    generate_file_result_with_vulnerability,
    generate_path_scan_collection,
)


@pytest.mark.parametrize(
    "collection,expected_type",
    [
        (generate_path_scan_collection([]), CollectionType.PathScan),
        (generate_diff_scan_collection([]), CollectionType.DiffScan),
    ],
)
def test_iac_path_scan_collection_type(
    collection: IaCScanCollection, expected_type: CollectionType
) -> None:
    """
    GIVEN an IaC scan collection
    THEN the type is either 'path_scan' or 'diff_scan'
    """
    assert collection.type == expected_type


@pytest.mark.parametrize(
    "collection",
    [
        generate_path_scan_collection([]),
        generate_diff_scan_collection([]),
    ],
)
def test_iac_scan_collection_has_no_results(collection: IaCScanCollection) -> None:
    """
    GIVEN an IaC scan collection with no result
    THEN has_results returns False
    """
    assert not collection.has_results


def test_iac_path_scan_collection_has_results() -> None:
    """
    GIVEN an IaC path scan collection with some results
    THEN has_results returns True
    """

    collection = generate_path_scan_collection(
        [generate_file_result_with_vulnerability()]
    )
    assert collection.has_results


def test_iac_diff_scan_collection_no_new_results() -> None:
    """
    GIVEN an IaC diff scan collection with some results in unchanged/deleted only
    THEN has_results returns False
    """
    collection = generate_diff_scan_collection(
        unchanged=[generate_file_result_with_vulnerability()],
        deleted=[generate_file_result_with_vulnerability()],
        new=[],
    )
    assert not collection.has_results


def test_iac_diff_scan_collection_new_results() -> None:
    """
    GIVEN an IaC diff scan collection with some results in new
    THEN has_results returns True
    """
    collection = generate_diff_scan_collection(
        [generate_file_result_with_vulnerability()]
    )
    assert collection.has_results
