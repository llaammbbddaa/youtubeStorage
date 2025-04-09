#!/usr/bin/env python3
import subprocess
import sys
from functools import reduce

def duration_to_seconds(duration):
    parts = list(map(int, duration.split(':')))
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:  # SS
        return parts[0]
    return 0

def calculate_storage(total_seconds, mp3_bitrate=128, mp4_bitrate=5000):
    # MP3 calculation (128 kbps default)
    mp3_size = (total_seconds * mp3_bitrate * 1000) / (8 * 1024**3)  # GB
    
    # MP4 calculation (5000 kbps default ~1080p)
    mp4_size = (total_seconds * mp4_bitrate * 1000) / (8 * 1024**3)  # GB
    
    return mp3_size, mp4_size

def main(channel_url):
    # Get durations using yt-dlp
    command = [
        'yt-dlp',
        '--get-duration',
        '--flat-playlist',
        channel_url
    ]
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching durations: {e}")
        sys.exit(1)
    
    durations = result.stdout.strip().split('\n')
    total_seconds = reduce(lambda acc, d: acc + duration_to_seconds(d), durations, 0)
    
    # Calculate storage estimates
    mp3_size, mp4_size = calculate_storage(total_seconds)
    
    # Print results

    channelName = ""
    hasPassed = False
    for i in channel_url:
        if (i == "@"):
            hasPassed = True
        if (hasPassed):
            channelName += i

    print(f"Channel Analysis: {channelName}")
    print(f"Total Videos:     {len(durations)}")
    print(f"Total Duration:   {total_seconds // 3600} hours {(total_seconds % 3600) // 60} minutes")
    print("\nStorage Estimates:")
    print(f"MP3 (128 kbps):   {mp3_size:.2f} GB")
    print(f"MP3 (320 kbps):   {calculate_storage(total_seconds, 320)[0]:.2f} GB")
    print(f"MP4 (1080p):      {mp4_size:.2f} GB (5 Mbps average)")
    print(f"MP4 (4K):         {calculate_storage(total_seconds, mp4_bitrate=25000)[1]:.2f} GB (25 Mbps average)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <YouTube Channel URL>")
        sys.exit(1)
    
    main(sys.argv[1])

