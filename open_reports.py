#!/usr/bin/env python3
"""
Script to open HTML reports in the browser.
"""

import os
import webbrowser
import glob
from datetime import datetime
import random

# Fun ASCII art for the terminal
ASCII_ART = """
  _____    _____   _____    ____           _____   _______   __  __           _____ _    _ _____ _   _ ______ 
 |  __ \  / ____| |  __ \  / __ \         / ____| |__   __| |  \/  |   /\    / ____| |  | |_   _| \ | |  ____|
 | |__) || |  __  | |__) || |  | |  _____| (___      | |    | \  / |  /  \  | |    | |__| | | | |  \| | |__   
 |  _  / | | |_ | |  _  / | |  | | |______|\___ \     | |    | |\/| | / /\ \ | |    |  __  | | | | . ` |  __|  
 | | \ \ | |__| | | | \ \ | |__| |         ____) |    | |    | |  | |/ ____ \| |____| |  | |_| |_| |\  | |____ 
 |_|  \_\ \_____| |_|  \_\ \____/         |_____/     |_|    |_|  |_/_/    \_\\_____|_|  |_|_____|_| \_|______|
                                                                                                              
"""

ROAST_QUOTES = [
    "Roasting AIs since they can't feel it anyway!",
    "Making fun of models that can't fight back since 2025!",
    "Where AIs come to get their parameters questioned!",
    "Exposing AI biases one roast at a time!",
    "We don't discriminate - we roast all models equally badly!",
    "The only place where AI hallucinations are actually entertaining!",
    "Turning AI failures into comedy gold since 2025!",
    "Where we judge models by their outputs, not their parameter count!"
]

def list_reports():
    """List all HTML reports in the test_results and memes directories."""
    test_results = glob.glob("test_results/*.html")
    meme_results = glob.glob("memes/*.html")
    
    all_reports = []
    
    # Print ASCII art and a random roast quote
    print("\033[95m" + ASCII_ART + "\033[0m")
    print("\033[93m" + random.choice(ROAST_QUOTES) + "\033[0m")
    print("\n\033[96mAVAILABLE REPORTS:\033[0m")
    print("\033[90m" + "=" * 80 + "\033[0m")
    
    # List test result reports
    print("\n\033[92mTEST RESULTS:\033[0m")
    for i, report in enumerate(sorted(test_results, reverse=True), 1):
        # Get file creation time
        creation_time = os.path.getctime(report)
        time_str = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
        
        # Get report type from filename
        report_name = os.path.basename(report)
        if "comparison" in report_name:
            report_type = "🔥 MODEL COMPARISON"
        elif "bias" in report_name:
            report_type = "⚖️ BIAS TEST"
        else:
            report_type = "🤖 SINGLE MODEL TEST"
        
        print(f"\033[97m{i}. {report_type}: {report_name}\033[0m")
        print(f"   \033[90mCreated: {time_str}\033[0m")
        all_reports.append(report)
    
    # List meme reports
    if meme_results:
        print("\n\033[92mMEMES:\033[0m")
        for i, report in enumerate(sorted(meme_results, reverse=True), len(all_reports) + 1):
            # Get file creation time
            creation_time = os.path.getctime(report)
            time_str = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\033[97m{i}. 🤣 MEME: {os.path.basename(report)}\033[0m")
            print(f"   \033[90mCreated: {time_str}\033[0m")
            all_reports.append(report)
    
    return all_reports

def open_report(report_path):
    """Open a report in the browser."""
    # Get absolute path
    abs_path = os.path.abspath(report_path)
    print(f"\n\033[92mOpening {os.path.basename(report_path)} in browser...\033[0m")
    
    # Convert to file:// URL
    file_url = f"file://{abs_path}"
    
    # Open in browser
    webbrowser.open(file_url)

def main():
    """Main function."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    
    all_reports = list_reports()
    
    if not all_reports:
        print("\n\033[91mNo reports found. Run some tests first!\033[0m")
        return
    
    while True:
        try:
            choice = input("\n\033[96mEnter report number to open (or 'q' to quit): \033[0m")
            
            if choice.lower() == 'q':
                print("\n\033[93mThanks for using AI Roast Machine! Come back to roast more models soon!\033[0m")
                break
            
            choice = int(choice)
            if 1 <= choice <= len(all_reports):
                open_report(all_reports[choice - 1])
            else:
                print(f"\033[91mPlease enter a number between 1 and {len(all_reports)}.\033[0m")
        except ValueError:
            print("\033[91mPlease enter a valid number or 'q' to quit.\033[0m")
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")

if __name__ == "__main__":
    main() 