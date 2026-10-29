import pytest
from unittest.mock import patch
import httpx
from app.services.destination_service import DestinationService
from app.services.destination_image_service import DestinationImageService


def test_jaipur_destination_photo():
    """Jaipur must return verified Amber Palace photo with Annie Spratt attribution."""
    dest = DestinationService.verify_destination("Jaipur")
    assert dest.verified is True
    assert "Jaipur" in dest.resolved_name
    assert dest.country == "India"
    assert dest.image_url is not None
    assert "unsplash.com" in dest.image_url
    assert dest.image_status == "verified"
    assert dest.photographer_name == "Annie Spratt"
    assert dest.photographer_url is not None


def test_goa_destination_photo():
    """Goa must return verified coastal photo with Sumit Sourav attribution."""
    dest = DestinationService.verify_destination("Goa")
    assert dest.verified is True
    assert "Goa" in dest.resolved_name
    assert dest.country == "India"
    assert dest.image_url is not None
    assert dest.image_status == "verified"
    assert dest.photographer_name == "Sumit Sourav"


def test_paris_destination_photo():
    """Paris must return verified Eiffel Tower photo with Anthony Delanoix attribution."""
    dest = DestinationService.verify_destination("Paris")
    assert dest.verified is True
    assert "Paris" in dest.resolved_name
    assert dest.country == "France"
    assert dest.image_url is not None
    assert dest.image_status == "verified"
    assert dest.photographer_name == "Anthony Delanoix"


def test_unfamiliar_destination_photo():
    """Unfamiliar destinations (e.g. Zurich) return verified destination photo with attribution."""
    dest = DestinationService.verify_destination("Zurich")
    assert dest.verified is True
    assert "Zurich" in dest.resolved_name
    assert dest.image_url is not None
    assert dest.image_status in ["verified", "api_result"]


def test_dynamic_geocoded_destination_photo_mocked():
    """
    Tests dynamic Nominatim geocoding and Wikipedia photo resolution for a previously unseen destination (Reykjavik).
    """
    mock_nominatim = [{
        "display_name": "Reykjavik, Capital Region, Iceland",
        "address": {"city": "Reykjavik", "country": "Iceland"},
        "lat": "64.1466",
        "lon": "-21.9426"
    }]
    mock_wiki = {
        "title": "Reykjavik",
        "type": "standard",
        "originalimage": {"source": "https://upload.wikimedia.org/wikipedia/commons/reykjavik.jpg"}
    }

    class MockResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code
        def json(self):
            return self._data

    def mock_get(url, *args, **kwargs):
        if "nominatim.openstreetmap.org" in url:
            return MockResponse(mock_nominatim)
        if "wikipedia.org" in url:
            return MockResponse(mock_wiki)
        return MockResponse({}, status_code=404)

    with patch("httpx.Client.get", side_effect=mock_get):
        dest = DestinationService.verify_destination("Reykjavik")
        assert dest.verified is True
        assert "Reykjavik" in dest.resolved_name
        assert dest.country == "Iceland"
        assert dest.image_url == "https://upload.wikimedia.org/wikipedia/commons/reykjavik.jpg"
        assert dest.image_status == "api_result"
        assert "Wikimedia Commons" in (dest.photographer_name or "")


def test_ambiguous_destination_name_handling():
    """
    Ambiguous destination names (e.g. 'Springfield') that resolve to disambiguation
    pages must not fabricate an unrelated image. Must return 'unavailable'.
    """
    url, source, photog, photog_url, status = DestinationImageService.resolve_destination_image(
        destination_name="Springfield",
        country=None,
        is_verified=True
    )
    # Ambiguous destination: either unavailable or exact verified match, never generic random image
    if status == "unavailable":
        assert url is None


def test_image_api_failure_graceful_fallback():
    """
    When the image API encounters a network failure or 500 error, it must return
    an 'unavailable' status with None for image_url, never crashing or breaking the app.
    """
    with patch("httpx.Client.get", side_effect=httpx.ConnectError("Network unreachable")):
        # Clear cache for isolated test
        test_key = "nonexistent_city_test_failure|"
        DestinationImageService._cache.pop(test_key, None)

        url, source, photog, photog_url, status = DestinationImageService.resolve_destination_image(
            destination_name="Nonexistent City Test Failure",
            country="Test Country",
            is_verified=True
        )
        assert url is None
        assert status == "unavailable"
        assert source in ["no_verified_photo_found", "unverified_destination"]


def test_unverified_destination_placeholder():
    """Unverified destinations must never fabricate a photo match."""
    url, source, photog, photog_url, status = DestinationImageService.resolve_destination_image(
        destination_name="Unverified Random Place",
        country=None,
        is_verified=False
    )
    assert url is None
    assert status == "unavailable"
    assert source == "unverified_destination"


def test_gibberish_destination_rejected():
    with pytest.raises(ValueError) as exc:
        DestinationService.verify_destination("asdfghjk")
    assert "could not be verified" in str(exc.value)


def test_numeric_gibberish_rejected():
    with pytest.raises(ValueError) as exc:
        DestinationService.verify_destination("1234567")
    assert "could not be verified" in str(exc.value)
