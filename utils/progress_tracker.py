#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Tracker
Swiv Pwogrè
"""

import time
from typing import Optional, Callable
from datetime import datetime, timedelta


class ProgressTracker:
    """Track progress of long-running operations"""
    
    def __init__(self, total_steps: int, description: str = "Processing"):
        """
        Initialize progress tracker
        
        Args:
            total_steps: Total number of steps
            description: Description of the operation
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.description = description
        self.start_time = None
        self.step_times = []
        self.callbacks = []
    
    def start(self):
        """Start tracking"""
        self.start_time = datetime.now()
        self.current_step = 0
        self.step_times = []
        print(f"\n🚀 {self.description}")
        print(f"   Total steps: {self.total_steps}")
        print(f"   Started: {self.start_time.strftime('%H:%M:%S')}")
    
    def update(self, step: int, message: str = ""):
        """
        Update progress
        
        Args:
            step: Current step number (1-indexed)
            message: Optional status message
        """
        self.current_step = step
        now = datetime.now()
        self.step_times.append(now)
        
        # Calculate progress
        progress_pct = (step / self.total_steps) * 100
        
        # Calculate ETA
        if len(self.step_times) > 1:
            elapsed = (now - self.start_time).total_seconds()
            avg_time_per_step = elapsed / step
            remaining_steps = self.total_steps - step
            eta_seconds = avg_time_per_step * remaining_steps
            eta = timedelta(seconds=int(eta_seconds))
        else:
            eta = "calculating..."
        
        # Build progress bar
        bar_length = 30
        filled = int(bar_length * progress_pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Print progress
        print(f"\r⏳ [{bar}] {progress_pct:.1f}% | Step {step}/{self.total_steps} | ETA: {eta}", end='')
        
        if message:
            print(f"\n   {message}")
        
        # Call callbacks
        for callback in self.callbacks:
            callback(step, self.total_steps, progress_pct)
    
    def complete(self, message: str = ""):
        """Mark as complete"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print(f"\n\n✅ {self.description} Complete!")
        print(f"   Duration: {duration}")
        print(f"   Ended: {end_time.strftime('%H:%M:%S')}")
        
        if message:
            print(f"   {message}")
    
    def add_callback(self, callback: Callable):
        """
        Add callback function
        
        Args:
            callback: Function(step, total, percent)
        """
        self.callbacks.append(callback)
    
    def get_stats(self) -> dict:
        """Get progress statistics"""
        if not self.start_time:
            return {}
        
        now = datetime.now()
        elapsed = (now - self.start_time).total_seconds()
        
        return {
            'total_steps': self.total_steps,
            'current_step': self.current_step,
            'progress_pct': (self.current_step / self.total_steps) * 100,
            'elapsed_seconds': elapsed,
            'elapsed_formatted': str(timedelta(seconds=int(elapsed))),
            'avg_time_per_step': elapsed / self.current_step if self.current_step > 0 else 0,
        }


class SimpleProgress:
    """Simple progress indicator without ETA"""
    
    def __init__(self, description: str = "Processing"):
        self.description = description
        self.symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.index = 0
        self.running = False
    
    def start(self):
        """Start progress indicator"""
        self.running = True
        print(f"\n{self.description}...", end='')
    
    def tick(self):
        """Update indicator"""
        if self.running:
            print(f"\r{self.symbols[self.index]} {self.description}...", end='')
            self.index = (self.index + 1) % len(self.symbols)
    
    def stop(self, success: bool = True):
        """Stop indicator"""
        self.running = False
        if success:
            print(f"\r✅ {self.description} - Done!")
        else:
            print(f"\r❌ {self.description} - Failed!")


# Example usage
if __name__ == "__main__":
    import random
    
    # Example 1: Progress Tracker
    print("Example 1: Progress Tracker")
    print("=" * 60)
    
    tracker = ProgressTracker(total_steps=10, description="Processing Books")
    tracker.start()
    
    for i in range(1, 11):
        time.sleep(random.uniform(0.2, 0.5))
        tracker.update(i, f"Processing book {i}")
    
    tracker.complete("All books processed successfully!")
    
    # Show stats
    print("\nStatistics:")
    stats = tracker.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Example 2: Simple Progress
    print("\n\nExample 2: Simple Progress")
    print("=" * 60)
    
    progress = SimpleProgress("Downloading file")
    progress.start()
    
    for _ in range(20):
        time.sleep(0.1)
        progress.tick()
    
    progress.stop(success=True)

