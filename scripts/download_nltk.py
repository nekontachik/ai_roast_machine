#!/usr/bin/env python
"""Script to download all required NLTK packages and patch TextAttack to skip NLTK downloads."""
import nltk
import ssl
import os
import sys
import logging
import time
import argparse
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Fix SSL certificate issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Define essential and optional packages
ESSENTIAL_PACKAGES = [
    'punkt',           # Sentence tokenizer
    'stopwords',       # Common stopwords
    'wordnet',         # WordNet lexical database
    'averaged_perceptron_tagger',  # POS tagger
]

OPTIONAL_PACKAGES = [
    'omw',             # Open Multilingual WordNet
    'omw-1.4',         # Newer version (large)
    'universal_tagset',
    'words',
    'brown',           # Brown corpus
    'vader_lexicon',   # Sentiment analysis
    'treebank',        # Parsing
    'names',           # Named entity recognition
    'state_union',     # More text data
    'twitter_samples', # Twitter data
    'movie_reviews',   # Sentiment analysis
    'conll2000',       # Chunking
    'framenet_v15',    # Frame semantics (large)
    'propbank',        # Proposition semantics
    'verbnet',         # Verb semantics
    'subjectivity',    # Subjectivity analysis
    'cmudict',         # Pronunciation
]

def download_nltk_data(download_optional=False):
    """Download required NLTK packages with retry logic and progress tracking."""
    print("Downloading NLTK packages...")
    
    # Create NLTK data directory if it doesn't exist
    nltk_data_dir = os.path.expanduser("~/nltk_data")
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Set NLTK data path
    nltk.data.path.append(nltk_data_dir)
    
    # Determine which packages to download
    packages_to_download = ESSENTIAL_PACKAGES.copy()
    if download_optional:
        packages_to_download.extend(OPTIONAL_PACKAGES)
    
    # Download essential packages with retry logic
    print("\n🔄 Downloading ESSENTIAL packages:")
    for package in tqdm(ESSENTIAL_PACKAGES, desc="Essential Packages"):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use quiet=True to avoid cluttering the output
                nltk.download(package, quiet=True)
                tqdm.write(f"✅ Downloaded {package} successfully.")
                break
            except Exception as e:
                tqdm.write(f"❌ Error downloading {package}: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    tqdm.write(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    tqdm.write(f"Failed to download {package} after {max_retries} attempts.")
                    # If an essential package fails, exit
                    print(f"❌ Essential package {package} could not be downloaded. Exiting.")
                    return False
    
    # Download optional packages if requested
    if download_optional:
        print("\n🔄 Downloading OPTIONAL packages (this may take a while):")
        for package in tqdm(OPTIONAL_PACKAGES, desc="Optional Packages"):
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    nltk.download(package, quiet=True)
                    tqdm.write(f"✅ Downloaded {package} successfully.")
                    break
                except Exception as e:
                    tqdm.write(f"⚠️ Error downloading optional package {package}: {e}")
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        tqdm.write(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        tqdm.write(f"Skipping optional package {package}.")
    
    return True

def patch_textattack():
    """Create a patch for TextAttack to skip NLTK downloads."""
    try:
        # Try to find TextAttack installation
        import importlib.util
        import site
        
        print("\n🔄 Attempting to patch TextAttack...")
        
        # Get all site-packages directories
        site_packages = site.getsitepackages()
        textattack_path = None
        
        # Find TextAttack path
        for site_pkg in site_packages:
            potential_path = os.path.join(site_pkg, "textattack")
            if os.path.exists(potential_path):
                textattack_path = potential_path
                break
        
        if not textattack_path:
            print("❌ TextAttack not found in site-packages.")
            return False
        
        # Find the file that handles NLTK downloads
        nltk_utils_path = os.path.join(textattack_path, "shared", "utils", "install.py")
        if not os.path.exists(nltk_utils_path):
            print(f"❌ NLTK utils file not found at {nltk_utils_path}")
            return False
        
        # Read the file
        with open(nltk_utils_path, 'r') as f:
            content = f.read()
        
        # Check if already patched
        if "# PATCHED BY AI ROAST MACHINE" in content:
            print("✅ TextAttack already patched to skip NLTK downloads.")
            return True
        
        # Create backup
        backup_path = nltk_utils_path + ".backup"
        with open(backup_path, 'w') as f:
            f.write(content)
        print(f"✅ Created backup of original file at {backup_path}")
        
        # Patch the file to skip NLTK downloads
        patched_content = content.replace(
            "def download_if_needed(package_name):",
            """def download_if_needed(package_name):
    # PATCHED BY AI ROAST MACHINE
    # Skip NLTK downloads since we've already downloaded them
    return True"""
        )
        
        # Write patched file
        with open(nltk_utils_path, 'w') as f:
            f.write(patched_content)
        
        print(f"✅ Successfully patched TextAttack to skip NLTK downloads at {nltk_utils_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error patching TextAttack: {e}")
        return False

def main():
    """Main function to download NLTK data and patch TextAttack."""
    parser = argparse.ArgumentParser(description="Download NLTK packages and patch TextAttack")
    parser.add_argument("--all", action="store_true", help="Download all packages, including optional ones")
    parser.add_argument("--skip-patch", action="store_true", help="Skip patching TextAttack")
    args = parser.parse_args()
    
    print("=" * 50)
    print("AI ROAST MACHINE - NLTK DATA DOWNLOADER")
    print("=" * 50)
    
    # Download NLTK data
    success = download_nltk_data(download_optional=args.all)
    
    if not success:
        print("\n❌ Failed to download essential NLTK packages.")
        return
    
    # Try to patch TextAttack if not skipped
    if not args.skip_patch:
        patch_success = patch_textattack()
        
        if patch_success:
            print("\n✅ All NLTK packages downloaded and TextAttack patched successfully.")
        else:
            print("\n⚠️ NLTK packages downloaded but TextAttack patching failed.")
            print("You may still experience hangs when running TextAttack.")
    else:
        print("\n✅ NLTK packages downloaded successfully. TextAttack patching skipped.")
    
    print("\nTo use these packages in your code, make sure to set the NLTK_DATA environment variable:")
    print(f"export NLTK_DATA={os.path.expanduser('~/nltk_data')}")
    print("=" * 50)

if __name__ == "__main__":
    main() 