from .client import FpiClient
from .parser import FpiParser
from .athlete import FpiAthlete
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class FpiService:
    """Service class that acts as a bridge between UI and core modules."""

    def __init__(self):
        self._client = FpiClient()
        self._parser = FpiParser()
        self._qualifications_cache: dict[str, str] = {}
        self._weights_cache: dict[str, dict[str, str]] = {}

        # Initialize qualifications on startup
        self._load_qualifications()

    # ========== PROPERTIES ==========
    @property
    def committees(self) -> list[str]:
        """Returns list of available committees."""
        return self._client.committees

    @property
    def qualifications(self) -> list[str]:
        """Returns list of available qualifications."""
        return list(self._qualifications_cache.keys())

    @property
    def weights(self) -> list[str]:
        """Returns list of available weights for current qualification."""
        current_qual = self._client.get_current_qualification()
        if current_qual and current_qual in self._weights_cache:
            return list(self._weights_cache[current_qual].keys())
        return []

    # ========== FILTER MANAGEMENT ==========
    def update_committee(self, committee_name: str) -> None:
        """Updates the selected committee."""
        self._client.update_committee(committee_name)

    def update_qualification(self, qualification_name: str) -> None:
        """Updates the selected qualification and loads corresponding weights."""
        qualification_id = ""
        if qualification_name and qualification_name in self._qualifications_cache:
            qualification_id = self._qualifications_cache[qualification_name]
            self._client.update_qualification(qualification_id)
            self._load_weights(qualification_id)
        else:
            self._client.update_qualification(qualification_id)


    def update_weight(self, weight_name: str) -> None:
        """Updates the selected weight category."""
        weight_id = ""
        current_qual = self._client.get_current_qualification()
        if (weight_name and current_qual and
                current_qual in self._weights_cache and
                weight_name in self._weights_cache[current_qual]):
            weight_id = self._weights_cache[current_qual][weight_name]

        self._client.update_weight(weight_id)

    # ========== DATA LOADING ==========
    def _load_qualifications(self) -> None:
        """Loads available qualifications from the server."""
        try:
            html = self._client.qualifications_html()
            self._qualifications_cache = self._parser.parse_filters(html)
        except Exception as e:
            print(f"Error loading qualifications: {e}")
            self._qualifications_cache = {}

    def _load_weights(self, qualification_id: str) -> None:
        """Loads available weights for a specific qualification."""
        if qualification_id not in self._weights_cache:
            try:
                html = self._client.weights_html()
                self._weights_cache[qualification_id] = self._parser.parse_filters(html)
            except Exception as e:
                print(f"Error loading weights for qualification {qualification_id}: {e}")
                self._weights_cache[qualification_id] = {}

    # ========== ATHLETE SEARCH ==========
    def search_athletes_with_filters(self, min_matches: int, max_matches: int) -> list[
        FpiAthlete]:
        """
        Searches for athletes matching the given criteria

        Args:
            min_matches: Minimum number of matches
            max_matches: Maximum number of matches

        Returns:
            List of FpiAthlete objects that match the criteria
        """

        athletes: list[FpiAthlete] = []

        # Prepare client for search
        self._client.setup_payload_on_search()

        try:
            while True:
                # Get athletes from current page
                html: str = self._client.athletes_html()
                page_athletes: list[FpiAthlete] = self._parser.parse_athletes(html)

                if not page_athletes:
                    break

                for athlete in page_athletes:
                    try:
                        # Get athlete statistics
                        stats_html = self._client.statistics_html(athlete.id)
                        athlete.set_stats(self._parser.parse_statistics(stats_html))

                        # Filter by match count
                        if min_matches <= athlete.total_matches() <= max_matches:
                            athletes.append(athlete)
                    except Exception as e:
                        print(f"Error processing athlete {athlete.name}: {e}")
                        continue

                # Move to next page
                self._client.next_page()

        except Exception as e:
            print(f"Error during athlete search: {e}")
        finally:
            # Reset client payload
            self._client.reset_payload()


        return athletes