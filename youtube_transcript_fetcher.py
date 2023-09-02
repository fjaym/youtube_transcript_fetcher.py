# Dependencies
import os
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Configuration
# Use environment variables for API keys for security reasons.
# This ensures that the API key isn't directly embedded in the code.
API_KEY = os.environ.get('YOUTUBE_API_KEY')  
CHANNEL_IDS = ['CHANNEL_ID_1', 'CHANNEL_ID_2', '...']  # Replace with the channel IDs of interest.

# Initialize the YouTube API.
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Main function to fetch and save transcripts from YouTube.
def fetch_transcripts():
    # Generate the filename using the current timestamp.
    output_file = f'{datetime.now().strftime("%Y%m%d%H%M")}_transcripts.txt'
    
    # Iterate through each channel to fetch videos.
    for channel_id in CHANNEL_IDS:
        # Fetch channel details to retrieve the 'uploads' playlist ID and the channel title.
        channel_response = youtube.channels().list(
            part='snippet,contentDetails',
            id=channel_id
        ).execute()

        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        channel_title = channel_response['items'][0]['snippet']['title']

        page_token = None
        break_flag = False  # Flag to break loop if videos older than 1 day are encountered.

        # Loop through pages of videos using pagination.
        while True and not break_flag:
            # Fetch videos from the 'uploads' playlist.
            # maxResults determines how many videos are fetched in a single API call.
            # It can be varied between 1 and 50 as per user preference. 
            # A higher value will fetch more videos in one go, but might consume more quota.
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=50,  # This can be modified based on user's needs.
                pageToken=page_token
            ).execute()

            # Iterate through each video and retrieve its transcript.
            for playlist_item in playlist_response['items']:
                video_id = playlist_item['snippet']['resourceId']['videoId']
                video_title = playlist_item['snippet']['title']

                # Convert the ISO 8601 formatted published date to a datetime object.
                published_at = playlist_item['snippet']['publishedAt']
                published_at_datetime = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                published_at_datetime = published_at_datetime.replace(tzinfo=timezone.utc)

                # Check if the video is older than a day.
                if published_at_datetime <= datetime.now(timezone.utc) - timedelta(days=1):
                    break_flag = True
                    break

                # Fetch the video transcript.
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    # Convert individual transcript lines into a single line/paragraph.
                    transcript_text = ' '.join([entry['text'] for entry in transcript])

                    # Write the details and transcript to the output file.
                    with open(output_file, 'a') as f:
                        f.write(f'\nChannel: {channel_title}\n')
                        f.write(f'Video Title: {video_title}\n')
                        f.write(f'Video ID: {video_id}\n')
                        f.write(transcript_text + '\n')

                except:
                    print(f'Error fetching transcript for video: {video_title} from channel: {channel_title}')

            # Handle pagination to fetch the next page of videos, if available.
            if 'nextPageToken' not in playlist_response or break_flag:
                break
            page_token = playlist_response['nextPageToken']

# Ensure the script runs the main function when executed.
if __name__ == "__main__":
    fetch_transcripts()
