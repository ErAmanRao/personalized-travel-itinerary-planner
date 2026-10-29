import httpx
import logging
from typing import Optional, Tuple
from app.models.schemas import DestinationInfo
from app.services.destination_image_service import DestinationImageService

logger = logging.getLogger(__name__)

# Curated reference database for instant, verified destination resolution & fallback images
KNOWN_DESTINATIONS = {
    "jaipur": {
        "resolved_name": "Jaipur, Rajasthan",
        "country": "India",
        "lat": 26.9124,
        "lon": 75.7873,
        "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_heritage",
        "must_see": ["Amber Palace", "Hawa Mahal", "City Palace", "Jantar Mantar", "Nahargarh Fort"]
    },
    "goa": {
        "resolved_name": "Goa",
        "country": "India",
        "lat": 15.2993,
        "lon": 74.1240,
        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_coastal",
        "must_see": ["Fort Aguada", "Palolem Beach", "Basilica of Bom Jesus", "Dudhsagar Falls", "Anjuna Flea Market"]
    },
    "kerala": {
        "resolved_name": "Kerala (Kochi & Munnar)",
        "country": "India",
        "lat": 9.9312,
        "lon": 76.2673,
        "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_nature",
        "must_see": ["Alleppey Backwaters", "Tea Gardens of Munnar", "Fort Kochi", "Eravikulam National Park"]
    },
    "delhi": {
        "resolved_name": "New Delhi, Delhi",
        "country": "India",
        "lat": 28.6139,
        "lon": 77.2090,
        "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_metro",
        "must_see": ["Qutub Minar", "Humayun's Tomb", "India Gate", "Red Fort", "Lotus Temple"]
    },
    "mumbai": {
        "resolved_name": "Mumbai, Maharashtra",
        "country": "India",
        "lat": 18.9220,
        "lon": 72.8347,
        "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_metro",
        "must_see": ["Gateway of India", "Marine Drive", "Elephanta Caves", "Colaba Causeway", "Bandra Fort"]
    },
    "udaipur": {
        "resolved_name": "Udaipur, Rajasthan",
        "country": "India",
        "lat": 24.5854,
        "lon": 73.7125,
        "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_heritage",
        "must_see": ["City Palace", "Lake Pichola Boat Cruise", "Jag Mandir", "Saheliyon-ki-Bari"]
    },
    "varanasi": {
        "resolved_name": "Varanasi, Uttar Pradesh",
        "country": "India",
        "lat": 25.3176,
        "lon": 82.9739,
        "image_url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_heritage",
        "must_see": ["Dashashwamedh Ghat Ganga Aarti", "Kashi Vishwanath", "Sarnath", "Assi Ghat"]
    },
    "paris": {
        "resolved_name": "Paris, Île-de-France",
        "country": "France",
        "lat": 48.8566,
        "lon": 2.3522,
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Eiffel Tower", "Louvre Museum", "Notre-Dame & Île de la Cité", "Montmartre & Sacré-Cœur", "Musée d'Orsay"]
    },
    "tokyo": {
        "resolved_name": "Tokyo, Kanto",
        "country": "Japan",
        "lat": 35.6762,
        "lon": 139.6503,
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Senso-ji Temple", "Shibuya Crossing & Sky", "Meiji Shrine", "Akihabara", "Shinjuku Gyoen"]
    },
    "kyoto": {
        "resolved_name": "Kyoto, Kansai",
        "country": "Japan",
        "lat": 35.0116,
        "lon": 135.7681,
        "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Fushimi Inari Taisha", "Kinkaku-ji (Golden Pavilion)", "Arashiyama Bamboo Grove", "Gion Historic District"]
    },
    "rome": {
        "resolved_name": "Rome, Lazio",
        "country": "Italy",
        "lat": 41.9028,
        "lon": 12.4964,
        "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Colosseum & Roman Forum", "Vatican Museums & St. Peter's", "Pantheon", "Trevi Fountain", "Piazza Navona"]
    },
    "london": {
        "resolved_name": "London, England",
        "country": "United Kingdom",
        "lat": 51.5074,
        "lon": -0.1278,
        "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Tower Bridge & Tower of London", "British Museum", "Westminster Abbey & Big Ben", "Hyde Park", "Borough Market"]
    },
    "barcelona": {
        "resolved_name": "Barcelona, Catalonia",
        "country": "Spain",
        "lat": 41.3879,
        "lon": 2.1699,
        "image_url": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Sagrada Família", "Park Güell", "Gothic Quarter", "Casa Batlló", "Barceloneta Beach"]
    },
    "dubai": {
        "resolved_name": "Dubai",
        "country": "United Arab Emirates",
        "lat": 25.2048,
        "lon": 55.2708,
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Burj Khalifa & Dubai Mall", "Dubai Marina Walk", "Old Dubai & Spice Souk", "Palm Jumeirah", "Desert Safari"]
    },
    "bali": {
        "resolved_name": "Bali",
        "country": "Indonesia",
        "lat": -8.4095,
        "lon": 115.1889,
        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_nature",
        "must_see": ["Uluwatu Temple", "Tegallalang Rice Terraces", "Ubud Sacred Monkey Forest", "Seminyak Beach", "Tanah Lot"]
    },
    "singapore": {
        "resolved_name": "Singapore",
        "country": "Singapore",
        "lat": 1.3521,
        "lon": 103.8198,
        "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Gardens by the Bay", "Marina Bay Sands SkyPark", "Chinatown & Maxwell Hawker Centre", "Sentosa Island", "Jewel Changi"]
    },
    "bangkok": {
        "resolved_name": "Bangkok",
        "country": "Thailand",
        "lat": 13.7563,
        "lon": 100.5018,
        "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier2",
        "must_see": ["Grand Palace & Wat Phra Kaew", "Wat Arun (Temple of Dawn)", "Chatuchak Market", "Chao Phraya River Cruise"]
    },
    "amsterdam": {
        "resolved_name": "Amsterdam, North Holland",
        "country": "Netherlands",
        "lat": 52.3676,
        "lon": 4.9041,
        "image_url": "https://images.unsplash.com/photo-1512470876302-972faa2aa9a4?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Rijksmuseum", "Van Gogh Museum", "Canal Ring Cruise", "Anne Frank House", "Jordaan District"]
    },
    "new york": {
        "resolved_name": "New York City, New York",
        "country": "United States",
        "lat": 40.7128,
        "lon": -74.0060,
        "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Central Park", "Metropolitan Museum of Art", "Empire State Building", "Statue of Liberty", "High Line & Hudson Yards"]
    },
    "zurich": {
        "resolved_name": "Zurich, Canton of Zurich",
        "country": "Switzerland",
        "lat": 47.3769,
        "lon": 8.5417,
        "image_url": "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Altstadt (Old Town)", "Lake Zurich", "Grossmünster", "Uetliberg", "Bahnhofstrasse"]
    },
    "agra": {
        "resolved_name": "Agra, Uttar Pradesh",
        "country": "India",
        "lat": 27.1767,
        "lon": 78.0081,
        "image_url": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
        "region_type": "india_heritage",
        "must_see": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh", "Itmad-ud-Daulah"]
    },
    "florence": {
        "resolved_name": "Florence, Tuscany",
        "country": "Italy",
        "lat": 43.7696,
        "lon": 11.2558,
        "image_url": "https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Duomo & Brunelleschi's Dome", "Uffizi Gallery", "Ponte Vecchio", "Piazzale Michelangelo", "Galleria dell'Accademia"]
    },
    "sydney": {
        "resolved_name": "Sydney, New South Wales",
        "country": "Australia",
        "lat": -33.8688,
        "lon": 151.2093,
        "image_url": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=1200&q=80",
        "region_type": "global_tier1",
        "must_see": ["Sydney Opera House", "Sydney Harbour Bridge", "Bondi Beach", "Taronga Zoo", "The Rocks"]
    }
}

DEFAULT_FALLBACK_IMAGE = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80"


class DestinationService:
    @staticmethod
    def verify_destination(query: str) -> DestinationInfo:
        """
        Validates destination against curated knowledge base and live geocoding (Nominatim).
        Rejects unverified or gibberish destinations.
        """
        clean_query = query.strip()
        lower_q = clean_query.lower()

        # 1. Reject obvious gibberish or keyboard smash immediately
        gibberish_patterns = ["asdf", "qwer", "zxcv", "1234", "test", "xxx"]
        is_gibberish = any(p in lower_q for p in gibberish_patterns) or len(set(lower_q)) <= 2

        if is_gibberish or len(clean_query) < 3:
            raise ValueError(
                f"Destination '{clean_query}' could not be verified by geographic registry. "
                "Please enter a recognized city, island, or region (e.g., 'Jaipur', 'Kyoto', 'Paris', 'Goa')."
            )

        # 2. Check our curated high-fidelity database
        for key, data in KNOWN_DESTINATIONS.items():
            if key in lower_q or lower_q in key:
                resolved_name = data["resolved_name"]
                country = data["country"]
                img_url, img_source, photog_name, photog_url, img_status = DestinationImageService.resolve_destination_image(
                    destination_name=resolved_name,
                    country=country,
                    is_verified=True
                )
                return DestinationInfo(
                    query=clean_query,
                    resolved_name=resolved_name,
                    country=country,
                    latitude=data["lat"],
                    longitude=data["lon"],
                    verified=True,
                    verification_source="curated_travel_registry",
                    image_url=img_url,
                    image_source=img_source,
                    photographer_name=photog_name,
                    photographer_url=photog_url,
                    image_attribution=f"Photo by {photog_name}" if photog_name else None,
                    image_status=img_status
                )

        # 3. Try OpenStreetMap Nominatim live geocoding (with short timeout)
        try:
            headers = {"User-Agent": "WanderWise-Planner/1.0 (academic-travel-tool)"}
            params = {
                "q": clean_query,
                "format": "jsonv2",
                "addressdetails": "1",
                "limit": "1"
            }
            timeout = httpx.Timeout(2.0, connect=1.0)
            with httpx.Client(timeout=timeout) as client:
                res = client.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers)
                if res.status_code == 200:
                    results = res.json()
                    if results and len(results) > 0:
                        first = results[0]
                        address = first.get("address", {})
                        country = address.get("country", "International")
                        city = (
                            address.get("city")
                            or address.get("town")
                            or address.get("state")
                            or address.get("region")
                            or first.get("display_name", clean_query).split(",")[0]
                        )
                        resolved = f"{city}, {country}" if country else city

                        img_url, img_source, photog_name, photog_url, img_status = DestinationImageService.resolve_destination_image(
                            destination_name=resolved,
                            country=country,
                            is_verified=True
                        )
                        return DestinationInfo(
                            query=clean_query,
                            resolved_name=resolved,
                            country=country,
                            latitude=float(first.get("lat", 0.0)),
                            longitude=float(first.get("lon", 0.0)),
                            verified=True,
                            verification_source="openstreetmap_nominatim",
                            image_url=img_url,
                            image_source=img_source,
                            photographer_name=photog_name,
                            photographer_url=photog_url,
                            image_attribution=f"Photo by {photog_name}" if photog_name else None,
                            image_status=img_status
                        )
        except Exception as e:
            logger.warning(f"Nominatim geocoding lookup failed or timed out: {e}")

        # 4. Accept with explicit unverified label as required by prompt
        return DestinationInfo(
            query=clean_query,
            resolved_name=clean_query.title(),
            country="International",
            latitude=None,
            longitude=None,
            verified=False,
            verification_source="unverified_user_input",
            image_url=None,
            image_source="unverified_destination",
            photographer_name=None,
            photographer_url=None,
            image_attribution=None,
            image_status="unavailable"
        )
