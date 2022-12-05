# Cloud function to get the leaderboard from a CSV in a Google Cloud Storage bucket
# and return it as a JSON object

import pandas as pd


def get_csv(bucket_name, csv_name):
    file = f"gs://{bucket_name}/{csv_name}"
    return pd.read_csv(file)

def parse_csv(csv):
    # Parse the CSV into a leaderboard
    leaderboard = csv.to_json(orient="records")

    # Return the leaderboard
    return leaderboard

# Get the leaderboard from the CSV
def get_leaderboard(bucket_name, csv_name):
    # Get the CSV from the bucket
    csv = get_csv(bucket_name, csv_name)

    # Parse the CSV into a leaderboard
    leaderboard = parse_csv(csv)

    # Return the leaderboard
    return leaderboard

def handler(request):
    bucket_name = request.args.get("bucket")

    if bucket_name is None:
        return "No bucket provided", 400

    # Get the leaderboard from the CSV
    try:
        leaderboard = get_leaderboard(bucket_name, 'leaderboard.csv')
    except Exception as e:
        return f"Error [{bucket_name}]: {e}", 500

    # Return the leaderboard as a JSON object
    return leaderboard
