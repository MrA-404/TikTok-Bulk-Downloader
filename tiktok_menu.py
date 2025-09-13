import os
import sys
import subprocess
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox

def display_menu():
    """
    Display the main menu with all options.
    """
    print("\n" + "="*50)
    print("TikTok Bulk Downloader - MRA Tools")
    print("="*50)
    print("1. Download videos from text file ")
    print("2. Grab all video links from a TikTok user")
    print("3. Rename downloaded videos")
    print("4. Organize videos into folders")
    print("5. Exit")
    print("="*50)

def run_downloader_gui():
    """
    Launch the GUI downloader script directly without cookies/watermark options.
    """
    try:
        import tiktok_downloader  # Ensure tiktok_downloader.py is in the same folder
        sys.argv = [sys.argv[0]]  # Clear any previous arguments
        tiktok_downloader.main()
    except Exception as e:
        print(f"Error launching downloader GUI: {e}")

def main():
    """
    Main function that displays the menu and handles user choices.
    """
    # Open Discord link when program starts
    webbrowser.open("https://discord.gg/BqNPP76Hvm")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            # Launch GUI downloader
            run_downloader_gui()
            
        elif choice == "2":
            # Grab video links
            username = input("Enter TikTok username (without @): ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            subprocess.run([sys.executable, "tiktok_link_grabber.py", username])
            
        elif choice == "3":
            # Rename videos
            directory = input("Enter directory containing videos to rename: ").strip()
            if not directory:
                print("Directory cannot be empty.")
                continue
            if not os.path.exists(directory):
                print(f"Directory '{directory}' does not exist.")
                continue
            subprocess.run([sys.executable, "tiktok_renamer.py", directory])
            
        elif choice == "4":
            # Organize videos
            directory = input("Enter directory containing videos to organize: ").strip()
            if not directory:
                print("Directory cannot be empty.")
                continue
            if not os.path.exists(directory):
                print(f"Directory '{directory}' does not exist.")
                continue
            try:
                videos_per_folder = int(input("Enter number of videos per folder: ").strip())
                if videos_per_folder <= 0:
                    print("Please enter a positive number.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
            subprocess.run([sys.executable, "tiktok_organizer.py", directory, str(videos_per_folder)])
            
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
