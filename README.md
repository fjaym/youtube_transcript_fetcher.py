## YouTube Transcript Fetcher

### Introduction:

This Python script fetches transcripts of the most recent videos (up to 24 hours old) from specified YouTube channels and consolidates them into a single text file.

### Features:

1. **Batch Processing**: Fetches transcripts from multiple channels in one go.
2. **Timestamp-based Filenaming**: Outputs are named based on the current timestamp for easy identification.
3. **Configurable Video Retrieval**: The number of videos fetched in a single API call can be customized.
4. **Error Handling**: Gracefully handles any issues that might arise during transcript retrieval.

### Prerequisites:

#### 1. Google Cloud Setup:

To use this script, you must set up the YouTube Data API v3 on Google Cloud Platform:

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project.
- Enable the YouTube Data API v3 for your project.
- Create API credentials (API Key) for your project.

#### 2. Dependencies:

You'll need to install the following Python libraries:

- `googleapiclient`
- `youtube_transcript_api`

You can use pip:

```bash
pip install --upgrade google-api-python-client youtube_transcript_api
```

### Configuration:

Replace `CHANNEL_IDS` in the script with the YouTube channel IDs of interest:
```python
CHANNEL_IDS = ['CHANNEL_ID_1', 'CHANNEL_ID_2', '...']
```

Also, ensure you set your YouTube API key as an environment variable for security:

```bash
export YOUTUBE_API_KEY='your_api_key_here'
```

### Usage:

Simply run the script:

```bash
python youtube_transcript_fetcher.py
```

The script will automatically create a `.txt` file with the fetched transcripts named based on the current timestamp.

### Customization:

1. **Modify Video Retrieval Count**: In the script, locate the line with `maxResults=50` inside the `youtube.playlistItems().list()` function call. Adjust the value (between 1 and 50) to fetch a different number of videos in one go.

### Troubleshooting:

- **API Quota Exceeded**: YouTube's API has daily quota limits. If you encounter a quota error, consider increasing the `maxResults` value to fetch more videos in one go, or wait for the quota to reset.
- **Video Transcript Errors**: Some videos may not have transcripts, or there may be other issues fetching them. These are gracefully handled, and an error message will be printed to the console.

---

I hope this version provides a more comprehensive guide for users.
