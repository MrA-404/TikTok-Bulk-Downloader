import os
import sys
import shutil
from pathlib import Path

def organize_videos(directory, videos_per_folder):
    """
    Organize videos into subfolders with a specified number of videos per folder.
    
    :param directory: Directory containing the videos
    :type directory: str
    :param videos_per_folder: Number of videos to put in each folder
    :type videos_per_folder: int
    """
    # Supported video extensions
    video_extensions = ['.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov']
    
    # Get all video files in the directory
    video_files = []
    for ext in video_extensions:
        video_files.extend(list(Path(directory).glob(f"*{ext}")))
    
    if not video_files:
        print(f"No video files found in {directory}")
        return
    
    print(f"Found {len(video_files)} video files to organize.")
    
    # Create folders and move videos
    folder_count = (len(video_files) // videos_per_folder) + 1
    folders_created = 0
    
    for i in range(folder_count):
        folder_name = f"Part_{i+1}"
        folder_path = Path(directory) / folder_name
        
        if not folder_path.exists():
            folder_path.mkdir()
            folders_created += 1
            print(f"Created folder: {folder_name}")
        
        # Calculate start and end indices for this folder
        start_idx = i * videos_per_folder
        end_idx = min((i + 1) * videos_per_folder, len(video_files))
        
        # Move videos to this folder
        for j in range(start_idx, end_idx):
            try:
                shutil.move(str(video_files[j]), str(folder_path / video_files[j].name))
                print(f"Moved: {video_files[j].name} -> {folder_name}/")
            except Exception as e:
                print(f"Error moving {video_files[j].name}: {e}")
    
    print(f"Organized {len(video_files)} videos into {folder_count} folders.")
    print(f"Created {folders_created} new folders.")

def main():
    """
    Main function for the organizer script.
    """
    if len(sys.argv) < 3:
        print("Usage: python tiktok_organizer.py <directory> <videos_per_folder>")
        return
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    
    try:
        videos_per_folder = int(sys.argv[2])
        if videos_per_folder <= 0:
            print("Please provide a positive number for videos per folder.")
            return
    except ValueError:
        print("Please provide a valid number for videos per folder.")
        return
    
    organize_videos(directory, videos_per_folder)

if __name__ == "__main__":
    main()