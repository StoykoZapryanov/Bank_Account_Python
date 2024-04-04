import pytest
from app.utils.data_loader import load_country_data, load_browser_data, load_platform_data, load_vertical_data
from app.utils.estimator import filter_data, calculate_traffic

def test_load_country_data():
    data = load_country_data()
    assert len(data) > 0

def test_load_browser_data():
    data = load_browser_data()
    assert len(data) > 0

def test_load_platform_data():
    data = load_platform_data()
    assert len(data) > 0

def test_load_vertical_data():
    data = load_vertical_data()
    assert len(data) > 0

def test_filter_data():
    data = pd.DataFrame({'country': ['US', 'UK', 'FR'], 'opps': [100, 200, 300]})
    filtered_data = filter_data(data, {'country': ['US', 'FR']})
    assert len(filtered_data) == 2

def test_calculate_traffic():
    data = pd.DataFrame({'opps': [100, 200, 300]})
    estimated_traffic = calculate_traffic(data, 1000)
    assert estimated_traffic == 333