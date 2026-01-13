"""
Terry Contact System - Contact management and support system
Handles customer support, issue tracking, and communication
"""

import os
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests

class TerryContactSystem:
    """Contact and support system for Terry-the-Tool-Bot"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.contacts_file = self.config_dir / "contacts.json"
        self.support_tickets_file = self.config_dir / "support_tickets.json"
        self.email_config = self._load_email_config()
        
        logging.info("Contact system initialized")
    
    def _get_config_dir(self) -> Path:
        """Get configuration directory"""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / 'Terry-the-Tool-Bot'
        else:  # Unix-like systems
            config_dir = Path.home() / '.config' / 'terry-tool-bot'
        
        config_dir.mkdir(exist_ok=True)
        return config_dir
    
    def _load_email_config(self) -> Dict[str, Any]:
        """Load email configuration"""
        config_file = self.config_dir / "email_config.json"
        
        default_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': 'terry-support@terry-tool-bot.dev',
            'smtp_password': '',
            'use_tls': True,
            'from_email': 'Terry Support <terry-support@terry-tool-bot.dev>',
            'contact_email': 'support@terry-tool-bot.dev'
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config
            except Exception as e:
                logging.error(f"Failed to load email config: {e}")
                return default_config
        
        return default_config
    
    def save_email_config(self, config: Dict[str, Any]) -> bool:
        """Save email configuration"""
        config_file = self.config_dir / "email_config.json"
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logging.info("Email configuration saved")
            return True
        except Exception as e:
            logging.error(f"Failed to save email config: {e}")
            return False
    
    def send_contact_email(self, to_email: str, subject: str, message: str, 
                           support_level: str = 'general') -> Dict[str, Any]:
        """Send contact email"""
        try:
            if not self.email_config['smtp_username'] or not self.email_config['smtp_password']:
                return {
                    'success': False,
                    'error': 'Email credentials not configured'
                }
            
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = to_email
            msg['Subject'] = f"[Terry Support - {support_level.title()}] {subject}"
            
            # Create message body
            body = MIMEText(message, 'plain')
            msg.attach(body)
            
            # Connect to SMTP server
            server = smtplib.SMTP(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            )
            
            if self.email_config['use_tls']:
                server.starttls()
            
            server.login(
                self.email_config['smtp_username'],
                self.email_config['smtp_password']
            )
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Contact email sent to {to_email}")
            
            # Log support interaction
            self._log_support_interaction(to_email, subject, support_level)
            
            return {
                'success': True,
                'message': f'Email sent to {to_email}'
            }
            
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_support_ticket(self, user_email: str, subject: str, description: str, 
                            priority: str = 'normal', category: str = 'general') -> Dict[str, Any]:
        """Create a new support ticket"""
        tickets = self._load_support_tickets()
        
        ticket = {
            'id': self._generate_ticket_id(),
            'user_email': user_email,
            'subject': subject,
            'description': description,
            'priority': priority,
            'category': category,
            'status': 'open',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'responses': []
        }
        
        tickets.append(ticket)
        self._save_support_tickets(tickets)
        
        logging.info(f"Support ticket created: {ticket['id']}")
        return ticket
    
    def _generate_ticket_id(self) -> str:
        """Generate unique ticket ID"""
        import uuid
        return f"TKT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    def _load_support_tickets(self) -> List[Dict[str, Any]]:
        """Load support tickets"""
        if self.support_tickets_file.exists():
            try:
                with open(self.support_tickets_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load support tickets: {e}")
                return []
        return []
    
    def _save_support_tickets(self, tickets: List[Dict[str, Any]]) -> bool:
        """Save support tickets"""
        try:
            with open(self.support_tickets_file, 'w') as f:
                json.dump(tickets, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Failed to save support tickets: {e}")
            return False
    
    def update_ticket_status(self, ticket_id: str, status: str, response: str = '', 
                         updated_by: str = 'system') -> Dict[str, Any]:
        """Update ticket status"""
        tickets = self._load_support_tickets()
        
        for ticket in tickets:
            if ticket['id'] == ticket_id:
                ticket['status'] = status
                ticket['updated_at'] = datetime.now().isoformat()
                ticket['responses'].append({
                    'response': response,
                    'updated_by': updated_by,
                    'timestamp': datetime.now().isoformat()
                })
                break
        
        return self._save_support_tickets(tickets)
    
    def get_ticket_by_id(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Get ticket by ID"""
        tickets = self._load_support_tickets()
        
        for ticket in tickets:
            if ticket['id'] == ticket_id:
                return ticket
        
        return None
    
    def get_open_tickets(self) -> List[Dict[str, Any]]:
        """Get all open tickets"""
        tickets = self._load_support_tickets()
        return [t for t in tickets if t.get('status') == 'open']
    
    def respond_to_ticket(self, ticket_id: str, response: str) -> Dict[str, Any]:
        """Respond to support ticket"""
        return self.update_ticket_status(ticket_id, 'answered', response, 'support_agent')
    
    def close_ticket(self, ticket_id: str, resolution: str) -> Dict[str, Any]:
        """Close support ticket"""
        return self.update_ticket_status(ticket_id, 'closed', resolution, 'system')
    
    def _log_support_interaction(self, email: str, subject: str, level: str) -> None:
        """Log support interaction for analytics"""
        try:
            log_file = self.config_dir / "support_log.json"
            
            interaction = {
                'email': email,
                'subject': subject,
                'level': level,
                'timestamp': datetime.now().isoformat()
            }
            
            logs = []
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append(interaction)
            
            # Keep only last 1000 interactions
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logging.error(f"Failed to log support interaction: {e}")
    
    def create_contact_request(self, name: str, email: str, message: str, 
                              request_type: str = 'general') -> Dict[str, Any]:
        """Create contact request"""
        contact = {
            'id': self._generate_ticket_id(),
            'name': name,
            'email': email,
            'message': message,
            'request_type': request_type,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        # Save to contacts
        contacts = self._load_contacts()
        contacts.append(contact)
        self._save_contacts(contacts)
        
        # Send confirmation email
        subject = f"Contact Request: {name}"
        body = f"""
Dear {name},

Thank you for reaching out to Terry-the-Tool-Bot support!

Your request details:
- Name: {name}
- Email: {email}
- Message: {message}
- Request Type: {request_type}
- Request ID: {contact['id']}
- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

We will review your request and get back to you within 24 hours.

Best regards,
Terry Support Team
        """
        
        self.send_contact_email(email, subject, body)
        
        logging.info(f"Contact request created: {contact['id']}")
        return contact
    
    def _load_contacts(self) -> List[Dict[str, Any]]:
        """Load contacts"""
        if self.contacts_file.exists():
            try:
                with open(self.contacts_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load contacts: {e}")
                return []
        return []
    
    def _save_contacts(self, contacts: List[Dict[str, Any]]) -> bool:
        """Save contacts"""
        try:
            with open(self.contacts_file, 'w') as f:
                json.dump(contacts, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Failed to save contacts: {e}")
            return False
    
    def get_contact_statistics(self) -> Dict[str, Any]:
        """Get contact statistics"""
        contacts = self._load_contacts()
        
        stats = {
            'total_contacts': len(contacts),
            'contact_requests_today': len([c for c in contacts if c['created_at'].startswith(datetime.now().strftime('%Y-%m-%d'))]),
            'pending_requests': len([c for c in contacts if c['status'] == 'pending']),
            'resolved_requests': len([c for c in contacts if c['status'] == 'resolved']),
            'average_response_time': '24 hours'  # Placeholder
        }
        
        return stats
    
    def send_newsletter(self, subject: str, content: str, subscribers: List[str]) -> Dict[str, Any]:
        """Send newsletter to subscribers"""
        successful_sends = 0
        failed_sends = []
        
        for subscriber in subscribers:
            try:
                result = self.send_contact_email(
                    subscriber,
                    f"Terry Newsletter: {subject}",
                    content,
                    'newsletter'
                )
                
                if result['success']:
                    successful_sends += 1
                else:
                    failed_sends.append({'email': subscriber, 'error': result.get('error')})
                    
            except Exception as e:
                failed_sends.append({'email': subscriber, 'error': str(e)})
        
        return {
            'success': True,
            'message': f"Newsletter sent to {len(subscribers)} subscribers",
            'successful_sends': successful_sends,
            'failed_sends': failed_sends
        }