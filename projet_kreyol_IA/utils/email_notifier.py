#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Notification System
Sistèm notifikasyon pa email
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional


class EmailNotifier:
    """Klas pou voye notifikasyon pa email / Class for email notifications"""
    
    def __init__(self):
        """Initialize email notifier"""
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("⚠️  Email config pa konplè / Email config incomplete")
            print("   Defini: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")
            self.enabled = False
        else:
            self.enabled = True
    
    def send_email(self, subject: str, body: str, html: bool = False) -> bool:
        """
        Voye yon email / Send an email
        
        Args:
            subject: Email subject
            body: Email body
            html: If True, send as HTML
        
        Returns:
            True if successful
        """
        if not self.enabled:
            print("⚠️  Email disabled - config missing")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # Attach body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email voye / Email sent to: {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Erè voye email / Email error: {e}")
            return False
    
    def notify_book_complete(self, book_name: str, urls: Dict[str, str]) -> bool:
        """
        Notifye pou yon liv fini / Notify when a book is complete
        
        Args:
            book_name: Name of the book
            urls: Dictionary of URLs (text, audio, podcast)
        
        Returns:
            True if successful
        """
        subject = f"✅ Liv fini / Book completed: {book_name}"
        
        # Plain text version
        body = f"""
Bonjou! / Hello!

Liv la fini trete: {book_name}

🔗 Lyen piblik yo / Public links:
"""
        
        for key, url in urls.items():
            body += f"\n{key.upper()}: {url}"
        
        body += f"""

Dat: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
Pwojè Kreyòl IA
Haitian Creole AI Project
"""
        
        # HTML version
        html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .links {{ background-color: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .link-item {{ margin: 10px 0; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ccc; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ Liv Fini / Book Completed</h1>
    </div>
    <div class="content">
        <h2>📚 {book_name}</h2>
        <p>Liv la fini trete avèk siksè! / The book has been processed successfully!</p>
        
        <div class="links">
            <h3>🔗 Lyen Piblik Yo / Public Links:</h3>
"""
        
        for key, url in urls.items():
            html_body += f'<div class="link-item"><strong>{key.upper()}:</strong><br><a href="{url}">{url}</a></div>'
        
        html_body += f"""
        </div>
        
        <p><strong>Dat / Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div class="footer">
        <p>Pwojè Kreyòl IA / Haitian Creole AI Project<br>
        🇭🇹 Powered by AI</p>
    </div>
</body>
</html>
"""
        
        return self.send_email(subject, html_body, html=True)
    
    def notify_batch_complete(self, results: List[Dict], duration: float) -> bool:
        """
        Notifye pou batch fini / Notify when batch is complete
        
        Args:
            results: List of processing results
            duration: Duration in seconds
        
        Returns:
            True if successful
        """
        completed = [r for r in results if r['status'] == 'completed']
        failed = [r for r in results if r['status'] == 'failed']
        
        subject = f"📦 Batch fini / Batch completed: {len(completed)}/{len(results)} liv"
        
        # Plain text version
        body = f"""
Bonjou! / Hello!

Batch processing fini!

📊 Rezime / Summary:
- Total liv / Total books: {len(results)}
- Konple / Completed: {len(completed)}
- Echwe / Failed: {len(failed)}
- Dire / Duration: {duration:.1f}s ({duration/60:.1f} min)

"""
        
        if completed:
            body += "\n✅ Liv konple / Completed books:\n"
            for r in completed:
                body += f"\n• {r['name']}\n"
                if r.get('urls'):
                    for key, url in r['urls'].items():
                        body += f"  {key}: {url}\n"
        
        if failed:
            body += "\n❌ Liv echwe / Failed books:\n"
            for r in failed:
                body += f"• {r['name']}: {', '.join(r.get('errors', []))}\n"
        
        body += f"""
Dat: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
Pwojè Kreyòl IA
"""
        
        # HTML version
        html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; min-width: 100px; }}
        .book-list {{ margin: 20px 0; }}
        .book-item {{ background-color: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
        .failed {{ border-left-color: #f44336; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ccc; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📦 Batch Processing Fini / Completed</h1>
    </div>
    <div class="content">
        <div class="stats">
            <div class="stat-box">
                <h3>{len(results)}</h3>
                <p>Total Liv</p>
            </div>
            <div class="stat-box">
                <h3>{len(completed)}</h3>
                <p>✅ Konple</p>
            </div>
            <div class="stat-box">
                <h3>{len(failed)}</h3>
                <p>❌ Echwe</p>
            </div>
            <div class="stat-box">
                <h3>{duration/60:.1f}</h3>
                <p>Minit</p>
            </div>
        </div>
"""
        
        if completed:
            html_body += '<div class="book-list"><h3>✅ Liv Konple / Completed Books:</h3>'
            for r in completed:
                html_body += f'<div class="book-item"><strong>{r["name"]}</strong><br>'
                if r.get('urls'):
                    for key, url in r['urls'].items():
                        html_body += f'{key}: <a href="{url}">{url}</a><br>'
                html_body += '</div>'
            html_body += '</div>'
        
        if failed:
            html_body += '<div class="book-list"><h3>❌ Liv Echwe / Failed Books:</h3>'
            for r in failed:
                html_body += f'<div class="book-item failed"><strong>{r["name"]}</strong><br>'
                html_body += f'Errors: {", ".join(r.get("errors", []))}</div>'
            html_body += '</div>'
        
        html_body += f"""
        <p><strong>Dat / Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div class="footer">
        <p>Pwojè Kreyòl IA / Haitian Creole AI Project<br>
        🇭🇹 Powered by AI</p>
    </div>
</body>
</html>
"""
        
        return self.send_email(subject, html_body, html=True)
    
    def notify_error(self, book_name: str, error_msg: str) -> bool:
        """
        Notifye pou erè / Notify about error
        
        Args:
            book_name: Name of the book
            error_msg: Error message
        
        Returns:
            True if successful
        """
        subject = f"❌ Erè / Error: {book_name}"
        
        body = f"""
Bonjou! / Hello!

Gen yon erè pandan pwosesis la / There was an error during processing:

📚 Liv / Book: {book_name}
❌ Erè / Error: {error_msg}

Dat: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
Pwojè Kreyòl IA
"""
        
        return self.send_email(subject, body)


# For testing
if __name__ == "__main__":
    notifier = EmailNotifier()
    
    if notifier.enabled:
        # Test simple notification
        urls = {
            'text': 'https://example.com/text.txt',
            'audio': 'https://example.com/audio.mp3',
            'podcast': 'https://example.com/podcast.mp3'
        }
        notifier.notify_book_complete("test_book", urls)
    else:
        print("❌ Email not configured")
        print("Set: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")

