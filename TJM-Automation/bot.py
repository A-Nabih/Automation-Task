"""
TJM Automation - Notepad Data Entry Bot

Automates data entry into Windows Notepad by fetching blog posts from API,
typing them into Notepad, and saving as individual text files.

Requirements:
- Windows OS with Notepad installed
- Python 3.7+ with required dependencies
- Internet connection for API calls

Version: 1.0.0
"""

import pyautogui
import pygetwindow as gw
import requests
import os
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import sys
from dotenv import load_dotenv

# Prefer robust implementation if available
try:
    from robust_automation import RobustNotepadBot
except Exception:
    RobustNotepadBot = None

# Load environment variables
load_dotenv('config.env')

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
log_file = os.getenv('LOG_FILE', 'tjm_automation.log')
enable_console = os.getenv('ENABLE_CONSOLE_LOGGING', 'true').lower() == 'true'

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout) if enable_console else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure pyautogui
pyautogui.FAILSAFE = os.getenv('ENABLE_FAILSAFE', 'true').lower() == 'true'
pyautogui.PAUSE = float(os.getenv('PYAUTOGUI_PAUSE', '0.5'))


class NotepadAutomationBot:
    """
    Automation bot for Notepad data entry operations.
    """
    
    def __init__(self):
        # Load configuration from environment variables
        self.api_url = os.getenv('API_URL', 'https://jsonplaceholder.typicode.com/posts')
        self.api_timeout = int(os.getenv('API_TIMEOUT', '30'))
        self.num_posts = int(os.getenv('NUM_POSTS', '10'))
        
        # File and directory settings
        output_dir_name = os.getenv('OUTPUT_DIR_NAME', 'tjm-project')
        self.output_dir = Path.home() / "Desktop" / output_dir_name
        
        # Automation timing settings
        self.window_wait_time = int(os.getenv('WINDOW_WAIT_TIME', '2'))
        self.save_dialog_wait = int(os.getenv('SAVE_DIALOG_WAIT', '1'))
        self.typing_interval = float(os.getenv('TYPING_INTERVAL', '0.01'))
        
        # File naming settings
        self.file_prefix = os.getenv('FILE_PREFIX', 'post')
        self.file_extension = os.getenv('FILE_EXTENSION', 'txt')
        
        # File handling settings
        self.file_conflict_action = os.getenv('FILE_CONFLICT_ACTION', 'overwrite').lower()
        
        # Development settings
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
        self.notepad_window = None
        
        if self.debug_mode:
            logger.info(f"Bot initialized - API: {self.api_url}, Posts: {self.num_posts}")
            logger.info(f"Output directory: {self.output_dir}")
            logger.info(f"File conflict action: {self.file_conflict_action}")
    
    def resolve_file_conflict(self, filepath: Path) -> Path:
        """
        Resolve file conflicts based on configuration.
        
        Args:
            filepath (Path): Original file path
            
        Returns:
            Path: Resolved file path
        """
        if not filepath.exists():
            return filepath
        
        if self.file_conflict_action == 'skip':
            logger.info(f"File {filepath.name} already exists, skipping...")
            return None
        
        elif self.file_conflict_action == 'overwrite':
            logger.info(f"File {filepath.name} already exists, will overwrite...")
            return filepath
        
        elif self.file_conflict_action == 'rename':
            counter = 1
            while True:
                new_name = f"{filepath.stem} ({counter}){filepath.suffix}"
                new_path = filepath.parent / new_name
                if not new_path.exists():
                    logger.info(f"File {filepath.name} already exists, renaming to {new_name}")
                    return new_path
                counter += 1
        
        
        else:
            logger.warning(f"Unknown file conflict action: {self.file_conflict_action}, defaulting to overwrite")
            return filepath
        
    def setup_output_directory(self) -> bool:
        """
        Create the output directory if it doesn't exist.
        
        Returns:
            bool: True if directory exists or was created successfully
        """
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output directory ready: {self.output_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to create output directory: {e}")
            return False
    
    def fetch_posts_from_api(self, limit: int = 10) -> List[Dict]:
        """
        Fetch blog posts from JSONPlaceholder API.
        
        Args:
            limit (int): Number of posts to fetch (default: 10)
            
        Returns:
            List[Dict]: List of post dictionaries
        """
        try:
            logger.info(f"Fetching {limit} posts from API...")
            response = requests.get(self.api_url, timeout=self.api_timeout)
            response.raise_for_status()
            
            posts = response.json()[:limit]
            logger.info(f"Successfully fetched {len(posts)} posts")
            return posts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching posts: {e}")
            return []
    
    def launch_notepad(self) -> bool:
        """
        Launch Windows Notepad application.
        
        Returns:
            bool: True if Notepad launched successfully
        """
        try:
            logger.info("Launching Notepad...")
            subprocess.Popen(['notepad.exe'])
            time.sleep(self.window_wait_time)  # Wait for Notepad to open
            
            # Find the Notepad window
            windows = gw.getWindowsWithTitle('Notepad')
            if windows:
                self.notepad_window = windows[0]
                self.notepad_window.activate()
                logger.info("Notepad launched and activated successfully")
                return True
            else:
                logger.error("Notepad window not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to launch Notepad: {e}")
            return False
    
    def type_text_safely(self, text: str) -> bool:
        """
        Type text into Notepad with error handling.
        
        Args:
            text (str): Text to type
            
        Returns:
            bool: True if typing was successful
        """
        try:
            # Ensure Notepad is active
            if self.notepad_window:
                self.notepad_window.activate()
                time.sleep(0.5)
            
            # Clear existing content (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)
            
            # Type the text
            pyautogui.write(text, interval=self.typing_interval)  # Configurable interval for natural typing
            logger.info("Text typed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False
    
    def save_file(self, filename: str) -> bool:
        """
        Save the current Notepad content to a file.
        
        Args:
            filename (str): Name of the file to save
            
        Returns:
            bool: True if file was saved successfully
        """
        try:
            # Check for file conflicts and resolve
            filepath = self.output_dir / filename
            resolved_path = self.resolve_file_conflict(filepath)
            
            if resolved_path is None:
                logger.info(f"File {filename} skipped due to conflict resolution")
                return True  # Return True because skipping is intentional
            
            # Update filename if it was renamed
            if resolved_path != filepath:
                filename = resolved_path.name
            
            # Ensure Notepad is active
            if self.notepad_window:
                self.notepad_window.activate()
                time.sleep(0.5)
            
            # Open Save As dialog (Ctrl+Shift+S)
            pyautogui.hotkey('ctrl', 'shift', 's')
            time.sleep(self.save_dialog_wait)
            
            # Navigate to output directory
            pyautogui.write(str(self.output_dir))
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Enter filename
            pyautogui.write(filename)
            pyautogui.press('enter')
            time.sleep(1)  # Wait longer for potential dialog
            
            # Handle file exists dialog - check if dialog appeared
            self._handle_file_exists_dialog()
            
            # Verify the file was actually saved
            final_filepath = self.output_dir / filename
            if final_filepath.exists():
                logger.info(f"File saved successfully: {filename}")
                return True
            else:
                logger.warning(f"File {filename} was not saved - file does not exist after save operation")
                return False
            
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {e}")
            return False
    
    def _handle_file_exists_dialog(self):
        """
        Handle the Windows file exists dialog that may appear when saving.
        """
        try:
            # Wait for dialog to appear
            time.sleep(0.5)
            
            # Try to confirm overwrite with Alt+Y (most common)
            pyautogui.hotkey('alt', 'y')
            time.sleep(0.3)
            logger.debug("Handled file exists dialog")
                
        except Exception as e:
            logger.warning(f"Error handling file exists dialog: {e}")
            # Fallback: just press Enter
            try:
                pyautogui.press('enter')
                time.sleep(0.5)
            except:
                pass
    
    def format_post_content(self, post: Dict) -> str:
        """
        Format a post dictionary into readable blog post format.
        
        Args:
            post (Dict): Post dictionary with 'title' and 'body' keys
            
        Returns:
            str: Formatted blog post content
        """
        title = post.get('title', 'Untitled Post')
        body = post.get('body', 'No content available.')
        
        formatted_content = f"""BLOG POST #{post.get('id', 'Unknown')}

        {title.upper()}

        {body}

        ---
        Generated by TJM Automation Bot
        Post ID: {post.get('id', 'Unknown')}
        User ID: {post.get('userId', 'Unknown')}
        """
        return formatted_content
    
    def process_single_post(self, post: Dict) -> bool:
        """
        Process a single post: type it into Notepad and save it.
        
        Args:
            post (Dict): Post dictionary to process
            
        Returns:
            bool: True if processing was successful
        """
        try:
            post_id = post.get('id', 'unknown')
            filename = f"{self.file_prefix} {post_id}.{self.file_extension}"
            
            logger.info(f"Processing post {post_id}...")
            
            # Format the post content
            content = self.format_post_content(post)
            
            # Type the content
            if not self.type_text_safely(content):
                return False
            
            # Save the file
            if not self.save_file(filename):
                return False
            
            logger.info(f"Successfully processed post {post_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process post {post.get('id', 'unknown')}: {e}")
            return False
    
    def run_automation(self, num_posts: int = 10) -> Dict[str, int]:
        """
        Run the complete automation process.
        
        Args:
            num_posts (int): Number of posts to process
            
        Returns:
            Dict[str, int]: Statistics of the automation run
        """
        stats = {
            'total_posts': 0,
            'successful_posts': 0,
            'failed_posts': 0
        }
        
        logger.info("Starting TJM Automation Bot...")
        
        # Step 1: Setup output directory
        if not self.setup_output_directory():
            logger.error("Failed to setup output directory. Aborting.")
            return stats
        
        # Step 2: Fetch posts from API
        posts = self.fetch_posts_from_api(num_posts)
        if not posts:
            logger.error("No posts fetched from API. Aborting.")
            return stats
        
        stats['total_posts'] = len(posts)
        
        # Dry run mode - just show what would be processed
        if self.dry_run:
            logger.info("DRY RUN MODE: Would process the following posts:")
            for post in posts:
                logger.info(f"  - Post {post.get('id')}: {post.get('title', 'No title')[:50]}...")
            return stats
        
        # Step 3: Launch Notepad
        if not self.launch_notepad():
            logger.error("Failed to launch Notepad. Aborting.")
            return stats
        
        # Step 4: Process each post
        logger.info(f"Starting to process {len(posts)} posts...")
        for i, post in enumerate(posts, 1):
            logger.info(f"Processing post {i}/{len(posts)}: Post ID {post.get('id', 'unknown')}")
            
            if self.process_single_post(post):
                stats['successful_posts'] += 1
                logger.info(f"Successfully processed post {i}/{len(posts)}")
            else:
                stats['failed_posts'] += 1
                logger.error(f"Failed to process post {i}/{len(posts)}")
            
            # Small delay between posts
            time.sleep(1)
        
        logger.info(f"Finished processing all {len(posts)} posts")
        
        # Step 5: Close Notepad
        try:
            if self.notepad_window:
                self.notepad_window.close()
                logger.info("Notepad closed successfully")
        except Exception as e:
            logger.warning(f"Failed to close Notepad: {e}")
        
        logger.info(f"Automation completed. Stats: {stats}")
        logger.info("Bot execution finished - exiting cleanly")
        return stats


def main():
    """
    Main function to run the automation bot.
    """
    try:
        # If robust implementation exists, prefer it
        if RobustNotepadBot is not None:
            api_url = os.getenv('API_URL', 'https://jsonplaceholder.typicode.com/posts')
            api_timeout = int(os.getenv('API_TIMEOUT', '30'))
            output_dir_name = os.getenv('OUTPUT_DIR_NAME', 'tjm-project')
            output_dir = Path.home() / "Desktop" / output_dir_name
            conflict_action = os.getenv('FILE_CONFLICT_ACTION', 'overwrite').lower()
            typing_interval = float(os.getenv('TYPING_INTERVAL', '0.01'))
            waits = {
                'window': float(os.getenv('WINDOW_WAIT_TIME', '2')),
                'save_dialog': float(os.getenv('SAVE_DIALOG_WAIT', '1')),
            }
            log_level = os.getenv('LOG_LEVEL', 'INFO')
            log_file = os.getenv('LOG_FILE', 'tjm_automation.log')
            file_prefix = os.getenv('FILE_PREFIX', 'post')
            file_extension = os.getenv('FILE_EXTENSION', 'txt')
            num_posts = int(os.getenv('NUM_POSTS', '10'))

            robust = RobustNotepadBot(
                api_url=api_url,
                api_timeout=api_timeout,
                output_dir=output_dir,
                conflict_action=conflict_action,
                typing_interval=typing_interval,
                waits=waits,
                log_file=log_file,
                log_level=log_level,
            )
            stats = robust.run(limit=num_posts, prefix=file_prefix, extension=file_extension)
            # Prepare pseudo-bot to reuse summary printing
            class _Tmp:
                def __init__(self, output_dir: Path):
                    self.output_dir = output_dir

            bot = _Tmp(output_dir)

        else:
            # Fallback to legacy implementation
            bot = NotepadAutomationBot()
            stats = bot.run_automation(num_posts=bot.num_posts)
        
        # Print final statistics
        print("\n" + "="*50)
        print("TJM AUTOMATION BOT - EXECUTION SUMMARY")
        print("="*50)
        print(f"Total Posts Processed: {stats['total_posts']}")
        print(f"Successful: {stats['successful_posts']}")
        print(f"Failed: {stats['failed_posts']}")
        print(f"Success Rate: {(stats['successful_posts']/stats['total_posts']*100):.1f}%" if stats['total_posts'] > 0 else "N/A")
        print(f"Output Directory: {bot.output_dir}")
        print("="*50)
        
        if stats['failed_posts'] == 0:
            print("🎉 All posts processed successfully!")
        else:
            print(f"⚠️  {stats['failed_posts']} posts failed to process. Check logs for details.")
        
        print("\nBot execution completed. Exiting...")
        logger.info("Main function completed successfully - exiting")
        
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
        print("\nAutomation interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()