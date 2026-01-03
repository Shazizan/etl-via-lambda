# GitHub ETL Pipeline: CSV to JSON Transfer Between Repositories
# This script demonstrates Extract, Transform, Load (ETL) process using lambda functions

# ============================================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================================

import requests  # Used to make HTTP requests to GitHub API
import json  # Used to work with JSON data format
import csv  # Used to parse CSV files
import base64  # GitHub API requires file content to be base64 encoded
from io import StringIO  # Allows us to treat strings as file objects

# ============================================================================
# STEP 2: CONFIGURATION - Replace with your actual values
# ============================================================================

# GitHub Personal Access Token - needed for authentication
# Generate at: https://github.com/settings/tokens (needs 'repo' scope)
GITHUB_TOKEN = "PLACE_YOUR_TOKEN"

# Source Repository Configuration (where CSV file is located)
SOURCE_OWNER = "Shazizan"  # GitHub username/org of source repo
SOURCE_REPO = "data"  # Name of source repository
SOURCE_FILE_PATH = "stocks_toy.csv"  # Path to CSV file in source repo

# Destination Repository Configuration (where JSON will be uploaded)
DEST_OWNER = "Shazizan"  # GitHub username/org of destination repo
DEST_REPO = "pipeline-vault"  # Name of destination repository
DEST_FILE_PATH = "stocks_toy.json"  # Path where JSON will be saved

# ============================================================================
# STEP 3: LAMBDA FUNCTIONS FOR ETL PROCESS
# ============================================================================

# Lambda function to create GitHub API headers
# Purpose: Adds authentication and specifies we're sending JSON
create_headers = lambda token: {
    "Authorization": f"Bearer {token}",  # Authenticates our request
    "Accept": "application/vnd.github.v3+json",  # Specifies GitHub API version
    "Content-Type": "application/json"  # Tells GitHub we're sending JSON
}

# Lambda function to construct GitHub API URL
# Purpose: Builds the correct URL to access files in a repository
build_url = lambda owner, repo, path: f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

# Lambda function to decode base64 content
# Purpose: GitHub returns file content in base64, this decodes it to text
decode_content = lambda content: base64.b64decode(content).decode('utf-8')

# Lambda function to encode content to base64
# Purpose: GitHub requires file uploads to be base64 encoded
encode_content = lambda content: base64.b64encode(content.encode('utf-8')).decode('utf-8')

# Lambda function to parse CSV to list of dictionaries
# Purpose: Converts CSV rows into Python dictionaries for easy manipulation
parse_csv = lambda csv_text: list(csv.DictReader(StringIO(csv_text)))

# Lambda function to convert list to JSON string
# Purpose: Transforms Python data structure into formatted JSON
to_json = lambda data: json.dumps(data, indent=2)  # indent=2 makes it readable

# ============================================================================
# STEP 4: EXTRACT FUNCTION
# ============================================================================

def extract_csv_from_github(owner, repo, file_path, token):
    """
    Extract CSV data from GitHub repository
    
    Args:
        owner: GitHub username or organization
        repo: Repository name
        file_path: Path to file within repository
        token: GitHub personal access token
    
    Returns:
        String content of the CSV file
    """
    
    # Build the API URL for the file
    url = build_url(owner, repo, file_path)
    
    # Create authentication headers
    headers = create_headers(token)
    
    # Make GET request to GitHub API
    print(f"📥 Extracting data from: {owner}/{repo}/{file_path}")
    response = requests.get(url, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse the JSON response
        file_data = response.json()
        
        # Decode the base64 content to get actual CSV text
        csv_content = decode_content(file_data['content'])
        
        print("✅ Extraction successful!")
        return csv_content
    else:
        # If request failed, raise an error with details
        raise Exception(f"❌ Failed to extract: {response.status_code} - {response.text}")

# ============================================================================
# STEP 5: TRANSFORM FUNCTION
# ============================================================================

def transform_csv_to_json(csv_content):
    """
    Transform CSV content to JSON format
    
    Args:
        csv_content: String content of CSV file
    
    Returns:
        JSON string representation of the data
    """
    
    print("🔄 Transforming CSV to JSON...")
    
    # Parse CSV text into list of dictionaries using lambda function
    data = parse_csv(csv_content)
    
    # Convert to JSON string using lambda function
    json_content = to_json(data)
    
    print(f"✅ Transformation complete! Converted {len(data)} rows")
    return json_content

# ============================================================================
# STEP 6: LOAD FUNCTION
# ============================================================================

def load_json_to_github(owner, repo, file_path, json_content, token, commit_message="ETL: Upload transformed data"):
    """
    Load JSON data to GitHub repository
    
    Args:
        owner: GitHub username or organization
        repo: Repository name
        file_path: Path where file should be saved
        json_content: JSON string to upload
        token: GitHub personal access token
        commit_message: Git commit message
    
    Returns:
        Response from GitHub API
    """
    
    print(f"📤 Loading data to: {owner}/{repo}/{file_path}")
    
    # Build the API URL for destination
    url = build_url(owner, repo, file_path)
    
    # Create authentication headers
    headers = create_headers(token)
    
    # First, check if file already exists (to get SHA for update)
    check_response = requests.get(url, headers=headers)
    
    # Prepare the payload for GitHub API
    payload = {
        "message": commit_message,  # Git commit message
        "content": encode_content(json_content),  # Base64 encoded content
        "branch": "main"  # Target branch (change if needed)
    }
    
    # If file exists, we need to include its SHA for update
    if check_response.status_code == 200:
        payload["sha"] = check_response.json()['sha']
        print("📝 File exists, updating...")
    else:
        print("📝 Creating new file...")
    
    # Make PUT request to create/update file
    response = requests.put(url, headers=headers, json=payload)
    
    # Check if upload was successful
    if response.status_code in [200, 201]:
        print("✅ Load successful!")
        return response.json()
    else:
        raise Exception(f"❌ Failed to load: {response.status_code} - {response.text}")

# ============================================================================
# STEP 7: MAIN ETL PIPELINE
# ============================================================================

def run_etl_pipeline():
    """
    Execute the complete ETL pipeline
    
    This function orchestrates the Extract, Transform, Load process
    """
    
    print("\n" + "="*60)
    print("🚀 Starting ETL Pipeline: GitHub CSV → JSON Transfer")
    print("="*60 + "\n")
    
    try:
        # EXTRACT: Get CSV data from source repository
        csv_data = extract_csv_from_github(
            owner=SOURCE_OWNER,
            repo=SOURCE_REPO,
            file_path=SOURCE_FILE_PATH,
            token=GITHUB_TOKEN
        )
        
        print()  # Empty line for readability
        
        # TRANSFORM: Convert CSV to JSON
        json_data = transform_csv_to_json(csv_data)
        
        print()  # Empty line for readability
        
        # LOAD: Upload JSON to destination repository
        result = load_json_to_github(
            owner=DEST_OWNER,
            repo=DEST_REPO,
            file_path=DEST_FILE_PATH,
            json_content=json_data,
            token=GITHUB_TOKEN,
            commit_message="ETL Pipeline: Automated CSV to JSON conversion"
        )
        
        print("\n" + "="*60)
        print("🎉 ETL Pipeline completed successfully!")
        print("="*60)
        print(f"\n📊 File uploaded to: {result['content']['html_url']}")
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"💥 ETL Pipeline failed: {str(e)}")
        print("="*60)

# ============================================================================
# STEP 8: EXECUTE THE PIPELINE
# ============================================================================

if __name__ == "__main__":
    # Run the ETL pipeline
    run_etl_pipeline()

# ============================================================================
# ADDITIONAL HELPER FUNCTIONS (Optional but useful)
# ============================================================================

# Lambda to validate GitHub token format
validate_token = lambda token: token.startswith(('ghp_', 'github_pat_'))

# Lambda to get file extension
get_extension = lambda filename: filename.split('.')[-1]

# Lambda to create timestamp for unique filenames
from datetime import datetime
create_timestamp = lambda: datetime.now().strftime("%Y%m%d_%H%M%S")

# Example: Create unique output filename with timestamp
# unique_filename = lambda base: f"{base}_{create_timestamp()}.json"
