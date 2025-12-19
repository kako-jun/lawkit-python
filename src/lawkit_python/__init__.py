"""
lawkit-python: Statistical law analysis toolkit for fraud detection and data quality

High-performance Benford, Pareto, Zipf, normal, and Poisson distribution analysis.
Powered by Rust for blazing fast performance.

Example:
    >>> import lawkit_python as lawkit
    >>> data = [123, 456, 789, 1234, 5678]
    >>> result = lawkit.law("benford", data)
    >>> print(result)
    [{'type': 'BenfordAnalysis', 'chi_square': 0.85, ...}]
"""

from __future__ import annotations

from typing import Any

# Import from native Rust module
try:
    from lawkit_python.lawkit_python import (
        __version__,
        law,
    )
except ImportError:
    # Fallback for development mode
    from lawkit_python import (  # type: ignore[attr-defined]
        __version__,
        law,
    )


class LawkitError(Exception):
    """Exception raised when a lawkit operation fails."""

    pass


def law_from_file(
    file_path: str, subcommand: str, **kwargs: Any
) -> list[dict[str, Any]]:
    """
    Analyze data from a file.

    Auto-detects file format and parses accordingly.

    Args:
        file_path: Path to the data file (JSON or CSV)
        subcommand: Analysis type ("benford", "pareto", "zipf", "normal", "poisson", etc.)
        **kwargs: Options passed to law() function

    Returns:
        List of analysis results

    Example:
        >>> result = law_from_file("data.json", "benford")
        >>> result = law_from_file("numbers.csv", "pareto", confidence_level=0.95)
    """
    import json
    from pathlib import Path

    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    ext = path.suffix.lower()

    # Try to parse based on extension
    if ext in {".json"}:
        data = json.loads(content)
    elif ext in {".csv", ".txt"}:
        # Parse as list of numbers (one per line or comma-separated)
        lines = content.strip().splitlines()
        data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Try comma-separated first
            if "," in line:
                for val in line.split(","):
                    val = val.strip()
                    if val:
                        try:
                            data.append(float(val))
                        except ValueError:
                            pass
            else:
                try:
                    data.append(float(line))
                except ValueError:
                    pass
    else:
        # Try JSON as fallback
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise LawkitError(f"Unsupported file format: {ext}") from e

    return law(subcommand, data, **kwargs)


def law_from_string(
    content: str, subcommand: str, format: str = "json", **kwargs: Any
) -> list[dict[str, Any]]:
    """
    Analyze data from a string.

    Args:
        content: Data string
        subcommand: Analysis type ("benford", "pareto", "zipf", "normal", "poisson", etc.)
        format: Content format ("json" or "csv")
        **kwargs: Options passed to law() function

    Returns:
        List of analysis results

    Example:
        >>> json_data = '{"values": [123, 456, 789]}'
        >>> result = law_from_string(json_data, "benford", format="json")
    """
    import json

    if format.lower() == "json":
        data = json.loads(content)
    elif format.lower() in {"csv", "txt"}:
        lines = content.strip().splitlines()
        data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if "," in line:
                for val in line.split(","):
                    val = val.strip()
                    if val:
                        try:
                            data.append(float(val))
                        except ValueError:
                            pass
            else:
                try:
                    data.append(float(line))
                except ValueError:
                    pass
    else:
        raise LawkitError(f"Unsupported format: {format}")

    return law(subcommand, data, **kwargs)


__all__ = [
    # Version
    "__version__",
    # Main function
    "law",
    # Utility functions
    "law_from_file",
    "law_from_string",
    # Exception
    "LawkitError",
]
