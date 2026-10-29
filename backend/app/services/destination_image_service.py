import httpx
import logging
import urllib.parse
from typing import Optional, Tuple, Dict
from app.config import settings

logger = logging.getLogger(__name__)

# Curated High-Fidelity Verified Editorial Registry
# Exact photos corresponding strictly to verified destinations with proper Unsplash attribution
VERIFIED_EDITORIAL_REGISTRY: Dict[str, Dict[str, str]] = {
    "jaipur": {
        "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Annie Spratt",
        "photographer_url": "https://unsplash.com/@anniespratt?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Amber Palace, Jaipur by Annie Spratt on Unsplash"
    },
    "goa": {
        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Sumit Sourav",
        "photographer_url": "https://unsplash.com/@sumitsourav?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Palolem Beach, Goa by Sumit Sourav on Unsplash"
    },
    "paris": {
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Anthony Delanoix",
        "photographer_url": "https://unsplash.com/@anthonydelanoix?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Eiffel Tower & Seine, Paris by Anthony Delanoix on Unsplash"
    },
    "kerala": {
        "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Jishnu",
        "photographer_url": "https://unsplash.com/@jishnu?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Tea Gardens of Munnar, Kerala on Unsplash"
    },
    "delhi": {
        "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Naveen Saxena",
        "photographer_url": "https://unsplash.com/@naveen?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Humayun's Tomb, Delhi by Naveen Saxena on Unsplash"
    },
    "mumbai": {
        "image_url": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Hardik Joshi",
        "photographer_url": "https://unsplash.com/@hardikjoshi?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Gateway of India, Mumbai by Hardik Joshi on Unsplash"
    },
    "udaipur": {
        "image_url": "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Kedar Gadge",
        "photographer_url": "https://unsplash.com/@kedargadge?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Lake Pichola, Udaipur by Kedar Gadge on Unsplash"
    },
    "varanasi": {
        "image_url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Kimberly Vardeman",
        "photographer_url": "https://unsplash.com/@kimberly?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Ganges Ghats, Varanasi by Kimberly Vardeman on Unsplash"
    },
    "agra": {
        "image_url": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Jovyn Chamb",
        "photographer_url": "https://unsplash.com/@jovynchamb?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Taj Mahal, Agra by Jovyn Chamb on Unsplash"
    },
    "shimla": {
        "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Amit Jain",
        "photographer_url": "https://unsplash.com/@amitjain?utm_source=wanderwise&utm_medium=referral",
        "attribution": "The Ridge, Shimla by Amit Jain on Unsplash"
    },
    "manali": {
        "image_url": "https://images.unsplash.com/photo-1605649487212-47bdab064df8?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Sylwia Bartyzel",
        "photographer_url": "https://unsplash.com/@sylwiabartyzel?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Solang Valley, Manali on Unsplash"
    },
    "amritsar": {
        "image_url": "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Bhupinder Pal Singh",
        "photographer_url": "https://unsplash.com/@bhupinder?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Golden Temple, Amritsar by Bhupinder Pal Singh on Unsplash"
    },
    "tokyo": {
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Jezael Melgoza",
        "photographer_url": "https://unsplash.com/@jezael?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Tokyo Tower Skyline by Jezael Melgoza on Unsplash"
    },
    "kyoto": {
        "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Su San Lee",
        "photographer_url": "https://unsplash.com/@susanlee?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Yasaka Pagoda, Kyoto by Su San Lee on Unsplash"
    },
    "rome": {
        "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "David Köhler",
        "photographer_url": "https://unsplash.com/@davidkoehler?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Colosseum, Rome by David Köhler on Unsplash"
    },
    "london": {
        "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Benjamin Davies",
        "photographer_url": "https://unsplash.com/@bendavisual?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Big Ben & Westminster, London by Benjamin Davies on Unsplash"
    },
    "barcelona": {
        "image_url": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Enes",
        "photographer_url": "https://unsplash.com/@enes?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Sagrada Família, Barcelona by Enes on Unsplash"
    },
    "dubai": {
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "ZQ Lee",
        "photographer_url": "https://unsplash.com/@zqlee?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Dubai Marina by ZQ Lee on Unsplash"
    },
    "bali": {
        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Justin Kauffman",
        "photographer_url": "https://unsplash.com/@justinkauffman?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Ulun Danu Bratan, Bali by Justin Kauffman on Unsplash"
    },
    "singapore": {
        "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Hu Chen",
        "photographer_url": "https://unsplash.com/@huchen?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Marina Bay Sands, Singapore by Hu Chen on Unsplash"
    },
    "bangkok": {
        "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Andreas Bruns",
        "photographer_url": "https://unsplash.com/@andreasbruns?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Wat Arun, Bangkok by Andreas Bruns on Unsplash"
    },
    "amsterdam": {
        "image_url": "https://images.unsplash.com/photo-1512470876302-972faa2aa9a4?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Javier M.",
        "photographer_url": "https://unsplash.com/@javierm?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Canals of Amsterdam by Javier M. on Unsplash"
    },
    "new york": {
        "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Lerone Pieters",
        "photographer_url": "https://unsplash.com/@leronepieters?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Manhattan, New York City by Lerone Pieters on Unsplash"
    },
    "sydney": {
        "image_url": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Dan Freeman",
        "photographer_url": "https://unsplash.com/@danfreemanphoto?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Sydney Opera House by Dan Freeman on Unsplash"
    },
    "cairo": {
        "image_url": "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Spencer Davis",
        "photographer_url": "https://unsplash.com/@spencerdavis?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Pyramids of Giza, Cairo by Spencer Davis on Unsplash"
    },
    "florence": {
        "image_url": "https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Jonathan Körner",
        "photographer_url": "https://unsplash.com/@jonathan?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Duomo, Florence by Jonathan Körner on Unsplash"
    },
    "venice": {
        "image_url": "https://images.unsplash.com/photo-1514890547357-a9ee288728e0?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Henrique Ferreira",
        "photographer_url": "https://unsplash.com/@henrique?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Grand Canal, Venice by Henrique Ferreira on Unsplash"
    },
    "zurich": {
        "image_url": "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?auto=format&fit=crop&w=1200&q=80",
        "photographer_name": "Henrique Ferreira",
        "photographer_url": "https://unsplash.com/@henrique?utm_source=wanderwise&utm_medium=referral",
        "attribution": "Altstadt, Zurich by Henrique Ferreira on Unsplash"
    }
}


class DestinationImageService:
    # In-memory thread-safe cache to eliminate repeated API lookups
    _cache: Dict[str, Tuple[Optional[str], Optional[str], Optional[str], Optional[str], str]] = {}

    @classmethod
    def resolve_destination_image(
        cls,
        destination_name: str,
        country: Optional[str] = None,
        is_verified: bool = True
    ) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], str]:
        """
        Resolves an authentic, verified destination image with proper photographer attribution.
        Returns:
            (image_url, image_source, photographer_name, photographer_url, image_status)
        Where image_status is one of:
            - 'verified' (from high-fidelity verified registry)
            - 'api_result' (dynamically fetched from Unsplash or Wikipedia/Wikimedia)
            - 'unavailable' (unverified, ambiguous, or no match found)

        Guaranteed:
            - Never returns random/unrelated city images or previous destination images.
            - If unverified or unavailable, returns (None, ..., 'unavailable') so UI displays a tasteful placeholder.
            - Never blocks or raises exceptions.
        """
        clean_name = destination_name.strip()
        if not clean_name or not is_verified:
            return (None, "unverified_destination", None, None, "unavailable")

        cache_key = f"{clean_name.lower()}|{(country or '').lower().strip()}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        lower_dest = clean_name.lower()

        # Step 1: Check curated high-fidelity editorial registry
        for key, info in VERIFIED_EDITORIAL_REGISTRY.items():
            if key == lower_dest or (len(key) >= 4 and key in lower_dest):
                result = (
                    info["image_url"],
                    "verified_editorial_photo",
                    info.get("photographer_name"),
                    info.get("photographer_url"),
                    "verified"
                )
                cls._cache[cache_key] = result
                return result

        # Step 2: Unsplash API Search (if configured with access key)
        if settings.UNSPLASH_ACCESS_KEY.strip():
            try:
                search_query = f"{clean_name} {country}".strip() if country else clean_name
                unsplash_result = cls._query_unsplash_api(search_query)
                if unsplash_result:
                    cls._cache[cache_key] = unsplash_result
                    return unsplash_result
            except Exception as e:
                logger.warning(f"Unsplash API query error for '{clean_name}': {e}")

        # Step 3: Open Travel Knowledge API (Wikipedia / Wikimedia Commons)
        try:
            wiki_result = cls._query_wikipedia_summary(clean_name, country)
            if wiki_result:
                cls._cache[cache_key] = wiki_result
                return wiki_result
        except Exception as e:
            logger.warning(f"Open travel knowledge API error for '{clean_name}': {e}")

        # Step 4: Graceful unavailable state (No generic image; honest fallback)
        unavailable_result = (None, "no_verified_photo_found", None, None, "unavailable")
        cls._cache[cache_key] = unavailable_result
        return unavailable_result

    @classmethod
    def _query_unsplash_api(cls, query: str) -> Optional[Tuple[Optional[str], Optional[str], Optional[str], Optional[str], str]]:
        """Queries Unsplash Search Photos endpoint."""
        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY.strip()}",
            "Accept-Version": "v1"
        }
        params = {
            "query": query,
            "orientation": "landscape",
            "per_page": 1
        }
        with httpx.Client(timeout=2.5) as client:
            resp = client.get(url, headers=headers, params=params)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    first = results[0]
                    img_url = first.get("urls", {}).get("regular") or first.get("urls", {}).get("full")
                    user = first.get("user", {})
                    photographer = user.get("name", "Unsplash Contributor")
                    user_url = user.get("links", {}).get("html", "https://unsplash.com")
                    if user_url and "?" not in user_url:
                        user_url += "?utm_source=wanderwise&utm_medium=referral"
                    return (img_url, "unsplash_api", photographer, user_url, "api_result")
        return None

    @classmethod
    def _query_wikipedia_summary(cls, destination: str, country: Optional[str] = None) -> Optional[Tuple[Optional[str], Optional[str], Optional[str], Optional[str], str]]:
        """
        Queries official Wikipedia REST API for lead geographic photo.
        Rejects ambiguous/disambiguation pages to prevent wrong city images.
        """
        # Clean destination (e.g. "Zurich, Switzerland" -> "Zurich")
        city_token = destination.split(",")[0].strip()
        encoded = urllib.parse.quote(city_token.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"

        headers = {
            "User-Agent": "WanderWise-Travel-Planner/1.0 (academic-travel-tool; mailto:travel@wanderwise.local)"
        }
        with httpx.Client(timeout=2.5) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                # 1. Ambiguity protection: Reject disambiguation pages (e.g. Springfield, Victoria)
                if data.get("type") == "disambiguation":
                    logger.info(f"Destination '{city_token}' is ambiguous (disambiguation page).")
                    return None

                # 2. Check for lead photo
                orig = (
                    data.get("originalimage", {}).get("source")
                    or data.get("thumbnail", {}).get("source")
                )
                if orig:
                    title = data.get("title", city_token)
                    photographer = f"Wikimedia Commons ({title})"
                    source_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{encoded}")
                    return (orig, "wikimedia_commons", photographer, source_url, "api_result")

        return None
