import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import lawkit
except ImportError:
    pytest.skip("lawkit module not built", allow_module_level=True)


class TestBasicAPI:
    """Test basic law() function"""

    def test_law_function_exists(self):
        assert hasattr(lawkit, "law")
        assert callable(lawkit.law)

    def test_returns_list(self):
        data = [123, 234, 345, 456, 567, 678, 789, 890, 901]
        results = lawkit.law("validate", data)
        assert isinstance(results, list)


class TestBenfordAnalysis:
    """Test Benford's law analysis"""

    def test_benford_analysis(self):
        data = [
            123, 234, 345, 156, 178, 189, 267, 289, 378,
            412, 523, 634, 745, 856, 967, 1234, 2345, 3456
        ]

        results = lawkit.law("benford", data)

        assert len(results) == 1
        result = results[0]
        assert result["type"] == "BenfordAnalysis"
        assert "observed_distribution" in result
        assert "expected_distribution" in result
        assert "chi_square" in result
        assert "p_value" in result
        assert "risk_level" in result


class TestParetoAnalysis:
    """Test Pareto analysis"""

    def test_pareto_analysis(self):
        data = [
            10000, 9000, 8000, 7000,
            1000, 900, 800, 700, 600, 500, 400, 300, 200, 100
        ]

        results = lawkit.law("pareto", data)

        assert len(results) == 1
        result = results[0]
        assert result["type"] == "ParetoAnalysis"
        assert "top_20_percent_contribution" in result
        assert "pareto_ratio" in result
        assert "concentration_index" in result


class TestZipfAnalysis:
    """Test Zipf analysis"""

    def test_zipf_analysis(self):
        data = [1000, 500, 333, 250, 200, 167, 143, 125, 111, 100]

        results = lawkit.law("zipf", data)

        assert len(results) == 1
        result = results[0]
        assert result["type"] == "ZipfAnalysis"
        assert "zipf_coefficient" in result
        assert "correlation_coefficient" in result


class TestNormalAnalysis:
    """Test normal distribution analysis"""

    def test_normal_analysis(self):
        data = [
            98, 99, 100, 101, 102, 99, 100, 101, 100, 99,
            101, 100, 99, 100, 101, 98, 102, 100, 99, 101
        ]

        results = lawkit.law("normal", data)

        assert len(results) == 1
        result = results[0]
        assert result["type"] == "NormalAnalysis"
        assert "mean" in result
        assert "std_dev" in result
        assert "skewness" in result
        assert "kurtosis" in result


class TestPoissonAnalysis:
    """Test Poisson distribution analysis"""

    def test_poisson_analysis(self):
        data = [0, 1, 2, 1, 3, 0, 2, 1, 4, 2, 1, 0, 3, 2, 1, 5, 0, 2, 1, 3]

        results = lawkit.law("poisson", data)

        assert len(results) == 1
        result = results[0]
        assert result["type"] == "PoissonAnalysis"
        assert "lambda" in result
        assert "variance_ratio" in result


class TestValidation:
    """Test data validation"""

    def test_validation(self):
        data = [123, 234, 345, 456, 567, 678, 789, 890, 901]

        results = lawkit.law("validate", data)

        assert len(results) == 1
        result = results[0]
        assert result["type"] == "ValidationResult"
        assert "validation_passed" in result
        assert "data_quality_score" in result


class TestOptions:
    """Test option handling"""

    def test_confidence_level_option(self):
        data = [123, 234, 345, 456, 567, 678, 789, 890, 901]

        results = lawkit.law("benford", data, confidence_level=0.99)

        assert len(results) == 1

    def test_risk_threshold_option(self):
        data = [123, 234, 345, 456, 567, 678, 789, 890, 901]

        results = lawkit.law("benford", data, risk_threshold="high")

        assert len(results) == 1


class TestErrorHandling:
    """Test error handling"""

    def test_unknown_subcommand(self):
        with pytest.raises(Exception):
            lawkit.law("unknown", [1, 2, 3])

    def test_empty_data(self):
        with pytest.raises(Exception):
            lawkit.law("benford", [])


if __name__ == "__main__":
    pytest.main([__file__])
