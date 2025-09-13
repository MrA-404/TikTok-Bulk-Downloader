import os
import re
import sys
from pathlib import Path

def rename_videos(directory):
    """
    Rename TikTok videos by removing only the date and uploader prefix.
    Keep hashtags and handle duplicate names by appending numbers.
    
    :param directory: Directory containing the videos
    :type directory: str
    """
    # Supported video extensions
    video_extensions = ['.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov', '.m4a']
    
    # Get all video files in the directory
    video_files = []
    for ext in video_extensions:
        video_files.extend(list(Path(directory).glob(f"*{ext}")))
    
    if not video_files:
        print(f"No video files found in {directory}")
        return
    
    print(f"Found {len(video_files)} video files to rename.")
    
    # Pattern to match the date and uploader prefix (e.g., "20250412 - everyday_kitchen101 - ")
    prefix_pattern = re.compile(r'^\d{8} - [\w\d_]+ - ')
    
    renamed_count = 0
    name_count = {}  # Track how many times we've seen each name
    
    for video_file in video_files:
        original_name = video_file.name
        
        # Remove only the date and uploader prefix, keep everything else including hashtags
        new_name = prefix_pattern.sub('', original_name)
        
        # If the pattern was found and removed
        if new_name != original_name:
            # Get the file extension
            name_without_ext, ext = os.path.splitext(new_name)
            
            # Count how many times we've seen this name
            if name_without_ext in name_count:
                name_count[name_without_ext] += 1
                new_name = f"{name_without_ext} {name_count[name_without_ext]}{ext}"
            else:
                name_count[name_without_ext] = 1
                new_name = f"{name_without_ext}{ext}"
            
            # Ensure the new filename is not too long (Windows limit is 255 chars)
            if len(new_name) > 200:
                name_without_ext, ext = os.path.splitext(new_name)
                new_name = name_without_ext[:200 - len(ext)] + ext
            
            # Rename the file
            try:
                new_path = video_file.parent / new_name
                
                # Check if the new filename already exists
                counter = 1
                base_name = new_name
                while new_path.exists():
                    name_without_ext, ext = os.path.splitext(base_name)
                    new_name = f"{name_without_ext} {counter}{ext}"
                    new_path = video_file.parent / new_name
                    counter += 1
                
                video_file.rename(new_path)
                print(f"Renamed: {original_name} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {original_name}: {e}")
        else:
            print(f"No changes needed for: {original_name}")
    
    print(f"Successfully renamed {renamed_count} files.")

def main():
    """
    Main function for the renamer script.
    """
    if len(sys.argv) < 2:
        print("Usage: python tiktok_renamer.py <directory>")
        return
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    
    rename_videos(directory)

if __name__ == "__main__":
    main()