import os
import sys
import subprocess
from datetime import datetime

def grab_user_video_links(username):
    """
    Grab all video links from a TikTok user's profile.
    
    :param username: TikTok username
    :type username: str
    :return: List of video URLs
    :rtype: list[str]
    """
    print(f"Grabbing video links for user: {username}")
    
    # Create a temporary directory for yt-dlp to work with
    temp_dir = f"temp_{username}"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Use yt-dlp to extract all video URLs from the user's profile
    try:
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "%(webpage_url)s",
            "--no-download",
            f"https://www.tiktok.com/@{username}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        links = result.stdout.strip().split('\n')
        links = [link for link in links if link.strip() != '']
        
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
            
        return links
    except Exception as e:
        print(f"Error grabbing links: {e}")
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        return []

def main():
    """
    Main function for the link grabber script.
    """
    if len(sys.argv) < 2:
        print("Usage: python tiktok_link_grabber.py <username>")
        return
    
    username = sys.argv[1]
    links = grab_user_video_links(username)
    
    if not links:
        print("No videos found for this user or an error occurred.")
        return
    
    # Save links to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{username}_videos_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(f"{link}\n")
    
    print(f"Saved {len(links)} video links to {output_file}")

if __name__ == "__main__":
    main()