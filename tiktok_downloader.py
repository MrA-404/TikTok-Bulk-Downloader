import os
import sys
import subprocess
import json
import csv
from datetime import datetime
import signal
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variable to track metadata during script execution
downloaded_metadata = []

# Global variable to prevent multiple retries
retry_attempted = False

def signal_handler(signal_received, frame):
    """
    Handle interruption signals (e.g., Ctrl-C).
    Save the downloaded metadata to the CSV file before exiting.
    """
    if downloaded_metadata:
        print("\nScript interrupted! Saving metadata for downloaded videos...")
        save_metadata_to_csv()
    print("Exiting gracefully.")
    sys.exit(0)

def save_metadata_to_csv():
    """
    Save the downloaded metadata to a CSV file.
    """
    if not downloaded_metadata:
        return  # No metadata to save

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    csv_file = f"{current_time}_download_log.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Upload Date", "Uploader", "Title", "URL", "Filename",
                         "Duration (sec)", "View Count", "Like Count", 
                         "Comment Count", "Repost Count", "Resolution"])
        writer.writerows(downloaded_metadata)
    print(f"Metadata saved to {csv_file}")

def clean_links_file(input_file):
    """
    Cleans the input links file by removing blank lines and prefixes.
    """
    cleaned_links = []
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("Date:"):
                    continue
                if line.startswith("Link: "):
                    line = line.replace("Link: ", "")
                cleaned_links.append(line)
    except Exception as e:
        print(f"Error reading or cleaning the input file: {e}")
    return cleaned_links

def download_with_ytdlp(links, download_dir):
    """
    Bulk-download TikTok videos and log metadata.
    """
    global retry_attempted
    print("Starting download_with_ytdlp function...")

    if not os.path.exists(download_dir):
        try:
            os.mkdir(download_dir)
            print(f"Created directory: {download_dir}")
        except Exception as e:
            print(f"Failed to create directory {download_dir}: {e}")
            return

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    failed_log_file = os.path.join(download_dir, f"{current_time}_failed_downloads_log.txt")

    total_links = len(links)
    successful_downloads = 0
    failed_downloads = 0
    failed_links = []

    for index, link in enumerate(links, start=1):
        try:
            print(f"\n[{index}/{total_links}]: {link}")

            output_template = os.path.join(
                download_dir,
                "%(upload_date).10s - %(uploader).50s - %(title).180B.%(ext)s"
            )

            cmd_download = ["yt-dlp", "--progress", "--no-warnings", "-o", output_template]
            cmd_download.append(link)

            subprocess.run(cmd_download, check=True)

            # Fetch metadata
            cmd_metadata = ["yt-dlp", "--dump-json", link]
            result = subprocess.run(cmd_metadata, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Failed to fetch metadata for {link}\n{result.stderr.strip()}")

            data = json.loads(result.stdout)
            upload_date = data.get("upload_date", "0000-00-00")
            formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}" if upload_date != "0000-00-00" else upload_date

            downloaded_metadata.append([
                formatted_date,
                data.get("uploader", "unknown_uploader"),
                data.get("title", "Untitled"),
                link,
                f"{formatted_date} - {data.get('uploader', 'unknown_uploader')} - {data.get('title', 'Untitled')}",
                data.get("duration", ""),
                data.get("view_count", ""),
                data.get("like_count", ""),
                data.get("comment_count", ""),
                data.get("repost_count", ""),
                f"{data.get('height', '')}p" if data.get("height") else "",
            ])

            print(" SUCCESS")
            successful_downloads += 1

        except Exception as e:
            print(" FAILED")
            failed_downloads += 1
            failed_links.append(link)
            with open(failed_log_file, "a", encoding="utf-8") as f:
                f.write(f"{link}\nError: {str(e).strip()}\n{'-' * 40}\n")

    if failed_links and not retry_attempted:
        retry_attempted = True
        print(f"\nRetrying {len(failed_links)} failed downloads...\n")
        download_with_ytdlp(failed_links, download_dir)
    elif failed_links:
        print("\nSome downloads still failed after retry. Check the failed log.")

    if not retry_attempted or not failed_links:
        save_metadata_to_csv()
        print("\nDownload process complete.")
        print(f"Successful: {successful_downloads}/{total_links}, Failed: {failed_downloads}/{total_links}")

def main():
    """
    Full GUI version: user selects links file and download folder.
    """
    signal.signal(signal.SIGINT, signal_handler)

    # GUI root
    root = tk.Tk()
    root.withdraw()  # Hide main window
    root.attributes("-topmost", True)  # Ensure dialogs appear on top

    # Select links file
    messagebox.showinfo("Select Links File", "Please select the links file containing TikTok URLs.")
    input_file = filedialog.askopenfilename(
        title="Select links file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        parent=root
    )
    if not input_file:
        print("No file selected. Exiting.")
        return

    links = clean_links_file(input_file)
    if not links:
        print("No valid links found in the selected file.")
        return

    # Select download folder
    messagebox.showinfo("Select Download Folder", "Please select the folder to save downloaded videos.")
    download_dir = filedialog.askdirectory(title="Select Download Folder", parent=root)
    if not download_dir:
        print("No folder selected. Exiting.")
        return

    print(f"Found {len(links)} links. Starting download...")
    download_with_ytdlp(links, download_dir)

if __name__ == "__main__":
    main()
