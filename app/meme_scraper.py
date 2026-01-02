"""
Automatic meme scraper to download fresh meme templates from the internet.
Ensures the meme library is always up-to-date with popular formats.
"""

import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

# Meme template URLs from popular sources (Imgflip, Know Your Meme)
MEME_TEMPLATE_URLS = {
    "drake_format.jpg": [
        "https://i.imgflip.com/30b1gx.jpg",
        "https://imgflip.com/s/meme/Drake-Hotline-Bling.jpg"
    ],
    "shocked_pikachu.jpg": [
        "https://i.imgflip.com/3c5j2u.jpg",
        "https://imgflip.com/s/meme/Surprised-Pikachu.jpg"
    ],
    "galaxy_brain.jpg": [
        "https://i.imgflip.com/2h7h1d.jpg",
        "https://imgflip.com/s/meme/Expanding-Brain.jpg"
    ],
    "clown_makeup.jpg": [
        "https://i.imgflip.com/38el31.jpg",
        "https://imgflip.com/s/meme/Clown-Applying-Makeup.jpg"
    ],
    "distracted_boyfriend.jpg": [
        "https://i.imgflip.com/1ur9b0.jpg",
        "https://imgflip.com/s/meme/Distracted-Boyfriend.jpg"
    ],
    "this_is_fine.jpg": [
        "https://i.imgflip.com/26am.jpg",
        "https://imgflip.com/s/meme/This-Is-Fine.jpg"
    ],
    "crying_cat.jpg": [
        "https://i.imgflip.com/2hgfw.jpg",
        "https://imgflip.com/s/meme/Sad-Cat.jpg"
    ],
    "stonks.jpg": [
        "https://i.imgflip.com/2yvad5.jpg",
        "https://i.imgflip.com/392xtu.jpg"
    ],
    "two_buttons.jpg": [
        "https://i.imgflip.com/1g8my4.jpg",
        "https://imgflip.com/s/meme/Two-Buttons.jpg"
    ],
    "is_this.jpg": [
        "https://i.imgflip.com/1h7in3.jpg",
        "https://imgflip.com/s/meme/Is-This-A-Pigeon.jpg"
    ],
    "woman_yelling_cat.jpg": [
        "https://i.imgflip.com/345v97.jpg",
        "https://imgflip.com/s/meme/Woman-Yelling-At-Cat.jpg"
    ],
    "success_kid.jpg": [
        "https://i.imgflip.com/1bhk.jpg",
        "https://imgflip.com/s/meme/Success-Kid.jpg"
    ],
    "uno_reverse.jpg": [
        "https://i.imgflip.com/3lmzyx.jpg",
        "https://imgflip.com/s/meme/UNO-Draw-25-Cards.jpg"
    ],
    "brain_meme.jpg": [
        "https://i.imgflip.com/2h7h1d.jpg",
        "https://imgflip.com/s/meme/Expanding-Brain.jpg"
    ]
}

class MemeScraper:
    """Handles automatic downloading and updating of meme templates."""

    def __init__(self, storage_dir: Path = None):
        """
        Initialize the meme scraper.

        Args:
            storage_dir: Directory to store downloaded memes. Defaults to static/memes/
        """
        if storage_dir is None:
            # Default to project's static/memes directory
            project_root = Path(__file__).parent.parent
            storage_dir = project_root / "static" / "memes"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Metadata file to track download dates
        self.metadata_file = self.storage_dir / ".meme_metadata.json"
        self.metadata = self._load_metadata()

        logger.info(f"MemeScraper initialized with storage: {self.storage_dir}")

    def _load_metadata(self) -> Dict:
        """Load meme download metadata from JSON file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load metadata: {e}")
                return {}
        return {}

    def _save_metadata(self):
        """Save meme download metadata to JSON file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")

    def download_meme(self, meme_name: str, url: str, timeout: int = 10) -> Optional[Path]:
        """
        Download a single meme from URL.

        Args:
            meme_name: Filename for the meme (e.g., "drake_format.jpg")
            url: URL to download from
            timeout: Request timeout in seconds

        Returns:
            Path to downloaded file, or None if failed
        """
        try:
            logger.info(f"Downloading {meme_name} from {url}")

            # Set user agent to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()

            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type:
                logger.warning(f"URL {url} returned non-image content: {content_type}")
                return None

            # Save to file
            file_path = self.storage_dir / meme_name
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Update metadata
            self.metadata[meme_name] = {
                'downloaded_at': datetime.now().isoformat(),
                'source_url': url,
                'size_bytes': file_path.stat().st_size
            }
            self._save_metadata()

            logger.info(f"Successfully downloaded {meme_name} ({file_path.stat().st_size} bytes)")
            return file_path

        except requests.RequestException as e:
            logger.error(f"Failed to download {meme_name} from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading {meme_name}: {e}")
            return None

    def download_meme_with_fallback(self, meme_name: str, urls: List[str]) -> Optional[Path]:
        """
        Try downloading a meme from multiple URLs until one succeeds.

        Args:
            meme_name: Filename for the meme
            urls: List of URLs to try in order

        Returns:
            Path to downloaded file, or None if all failed
        """
        for url in urls:
            result = self.download_meme(meme_name, url)
            if result:
                return result
            time.sleep(1)  # Brief delay between retries

        logger.error(f"All download URLs failed for {meme_name}")
        return None

    def download_all_templates(self, force_refresh: bool = False) -> Dict[str, Path]:
        """
        Download all meme templates from predefined URLs.

        Args:
            force_refresh: If True, re-download even if files exist

        Returns:
            Dictionary mapping meme names to downloaded file paths
        """
        results = {}

        for meme_name, urls in MEME_TEMPLATE_URLS.items():
            file_path = self.storage_dir / meme_name

            # Skip if already exists and not forcing refresh
            if file_path.exists() and not force_refresh:
                logger.info(f"Skipping {meme_name} (already exists)")
                results[meme_name] = file_path
                continue

            # Download with fallback URLs
            downloaded_path = self.download_meme_with_fallback(meme_name, urls)
            if downloaded_path:
                results[meme_name] = downloaded_path

            # Rate limiting - be polite to servers
            time.sleep(0.5)

        logger.info(f"Downloaded {len(results)}/{len(MEME_TEMPLATE_URLS)} memes")
        return results

    def auto_update_library(self, max_age_days: int = 30) -> Dict[str, str]:
        """
        Automatically update memes older than specified days.

        Args:
            max_age_days: Update memes older than this many days

        Returns:
            Dictionary with update status for each meme
        """
        results = {}
        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        for meme_name, urls in MEME_TEMPLATE_URLS.items():
            file_path = self.storage_dir / meme_name

            # Check if needs update
            needs_update = False

            if not file_path.exists():
                needs_update = True
                reason = "missing"
            elif meme_name in self.metadata:
                download_date = datetime.fromisoformat(self.metadata[meme_name]['downloaded_at'])
                if download_date < cutoff_date:
                    needs_update = True
                    reason = f"older than {max_age_days} days"
            else:
                # No metadata, check file modification time
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mtime < cutoff_date:
                    needs_update = True
                    reason = "no metadata, file old"

            if needs_update:
                logger.info(f"Updating {meme_name}: {reason}")
                downloaded_path = self.download_meme_with_fallback(meme_name, urls)
                results[meme_name] = "updated" if downloaded_path else "failed"
                time.sleep(0.5)  # Rate limiting
            else:
                results[meme_name] = "up-to-date"

        return results

    def check_missing_memes(self) -> List[str]:
        """
        Check which meme templates are missing from storage.

        Returns:
            List of missing meme filenames
        """
        missing = []
        for meme_name in MEME_TEMPLATE_URLS.keys():
            file_path = self.storage_dir / meme_name
            if not file_path.exists():
                missing.append(meme_name)
        return missing

    def get_meme_info(self, meme_name: str) -> Optional[Dict]:
        """
        Get information about a specific meme.

        Args:
            meme_name: Name of the meme file

        Returns:
            Dictionary with meme info, or None if not found
        """
        file_path = self.storage_dir / meme_name

        if not file_path.exists():
            return None

        info = {
            'name': meme_name,
            'path': str(file_path),
            'size_bytes': file_path.stat().st_size,
            'exists': True
        }

        # Add metadata if available
        if meme_name in self.metadata:
            info.update(self.metadata[meme_name])
        else:
            # Fallback to file stats
            info['downloaded_at'] = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat()

        return info

    def get_all_memes_status(self) -> Dict[str, Dict]:
        """
        Get status of all known meme templates.

        Returns:
            Dictionary mapping meme names to their info
        """
        status = {}
        for meme_name in MEME_TEMPLATE_URLS.keys():
            status[meme_name] = self.get_meme_info(meme_name) or {
                'name': meme_name,
                'exists': False
            }
        return status


def auto_download_memes_on_startup(max_age_days: int = 30) -> Dict[str, str]:
    """
    Convenience function to auto-download/update memes on app startup.

    Args:
        max_age_days: Update memes older than this many days

    Returns:
        Dictionary with download/update results
    """
    logger.info("Starting automatic meme library update...")
    scraper = MemeScraper()

    # Check for missing memes first
    missing = scraper.check_missing_memes()
    if missing:
        logger.info(f"Found {len(missing)} missing memes, downloading...")

    # Auto-update library
    results = scraper.auto_update_library(max_age_days=max_age_days)

    # Log summary
    updated = sum(1 for status in results.values() if status == "updated")
    failed = sum(1 for status in results.values() if status == "failed")
    up_to_date = sum(1 for status in results.values() if status == "up-to-date")

    logger.info(f"Meme library update complete: {updated} updated, {failed} failed, {up_to_date} up-to-date")

    return results


if __name__ == "__main__":
    # Test the scraper
    logging.basicConfig(level=logging.INFO)

    print("Testing MemeScraper...")
    scraper = MemeScraper()

    print("\nChecking current meme status:")
    status = scraper.get_all_memes_status()
    for meme_name, info in status.items():
        exists = "[OK]" if info['exists'] else "[MISSING]"
        print(f"  {exists} {meme_name}")

    print("\nDownloading missing memes...")
    results = scraper.auto_update_library(max_age_days=30)

    print("\nDownload results:")
    for meme_name, status in results.items():
        print(f"  {meme_name}: {status}")

    print("\nFinal status:")
    status = scraper.get_all_memes_status()
    total = len(status)
    existing = sum(1 for info in status.values() if info['exists'])
    print(f"  {existing}/{total} memes available")
