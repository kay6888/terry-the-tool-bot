"""
Terry Payment System - Cash App integration and donation management
Handles PayPal donations, Cash App purchases, and revenue tracking
"""

import os
import json
import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

class TerryPaymentSystem:
    """Payment and donation system for Terry-the-Tool-Bot"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.payments_file = self.config_dir / "payments.json"
        self.paypal_config = self._load_paypal_config()
        
        logging.info("Payment system initialized")
    
    def _get_config_dir(self) -> Path:
        """Get configuration directory"""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / 'Terry-the-Tool-Bot'
        else:  # Unix-like systems
            config_dir = Path.home() / '.config' / 'terry-tool-bot'
        
        config_dir.mkdir(exist_ok=True)
        return config_dir
    
    def _load_paypal_config(self) -> Dict[str, Any]:
        """Load PayPal configuration"""
        config_file = self.config_dir / "paypal_config.json"
        
        default_config = {
            'client_id': '',
            'client_secret': '',
            'sandbox_mode': True,
            'return_url': '',
            'webhook_url': '',
            'currency': 'USD',
            'donation_types': ['one_time', 'monthly', 'custom'],
            'default_amount': 10
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config
            except Exception as e:
                logging.error(f"Failed to load PayPal config: {e}")
                return default_config
        
        return default_config
    
    def _save_paypal_config(self, config: Dict[str, Any]) -> bool:
        """Save PayPal configuration"""
        config_file = self.config_dir / "paypal_config.json"
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logging.info("PayPal configuration saved")
            return True
        except Exception as e:
            logging.error(f"Failed to save PayPal config: {e}")
            return False
    
    def create_paypal_order(self, amount: float, description: str, 
                            custom_amount_id: Optional[str] = None,
                            return_url: Optional[str] = None) -> Dict[str, Any]:
        """Create PayPal donation order"""
        if not self.paypal_config['client_id']:
            return {
                'success': False,
                'error': 'PayPal not configured'
            }
        
        # PayPal API endpoint based on mode
        base_url = 'https://api-m.sandbox.paypal.com' if self.paypal_config['sandbox_mode'] else 'https://api-m.paypal.com'
        
        order_data = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': str(amount),
                    'description': description,
                    'reference_id': custom_amount_id or f'TERRY-{datetime.now().strftime("%Y%m%d")}'
                }
            ],
            'application_context': {
                'user_action': 'PAY',
                'payment_initiation': {
                    'return_url': return_url,
                    'cancel_url': f"{base_url}/v1/billing/subscriptions/{self.paypal_config['client_id']}/cancel"
                }
            },
            'brand_name': 'Terry-the-Tool-Bot'
            'locale': 'en-US',
            'logo_url': 'https://your-domain.com/logo.png',
            'customer_service': {
                'email': 'support@terry-tool-bot.dev',
                'phone': '+1-800-TERRY-TOOL'
            },
            'return_url': f"{base_url}/v1/billing/subscriptions/{self.paypal_config['client_id']}/agreement"
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._generate_paypal_token()}',
            'PayPal-Request-Id': self._generate_request_id()
        }
        
        try:
            response = requests.post(
                f"{base_url}/v1/checkout/orders",
                json=order_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 201:
                order_response = response.json()
                payment_info = self._save_payment_record(
                    'paypal',
                    amount,
                    description,
                    order_response,
                    custom_amount_id
                )
                
                return {
                    'success': True,
                    'order_id': order_response.get('id'),
                    'approval_url': order_response.get('links', {}).get('approve', [{}])[0].get('href'),
                    'payment_info': payment_info,
                    'message': 'PayPal order created successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to create PayPal order: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"PayPal order creation failed: {str(e)}"
            }
    
    def _generate_paypal_token(self) -> str:
        """Generate PayPal OAuth token"""
        # This would require OAuth 2.0 flow - simplified for this implementation
        # In production, you'd implement proper OAuth flow
        import base64
        auth_string = f"{self.paypal_config['client_id']}:{self.paypal_config['client_secret']}"
        return base64.b64encode(auth_string.encode()).decode()
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _save_payment_record(self, method: str, amount: float, description: str, 
                           order_response: Dict[str, Any], custom_id: Optional[str] = None) -> Dict[str, Any]:
        """Save payment record to database"""
        payment_info = {
            'method': method,
            'amount': amount,
            'description': description,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'paypal_order_id': order_response.get('id'),
            'custom_amount_id': custom_id,
            'order_response': order_response
        }
        
        # Load existing payments
        payments = self._load_payments()
        payments.append(payment_info)
        
        # Save payments
        self._save_payments(payments)
        
        return payment_info
    
    def _load_payments(self) -> List[Dict[str, Any]]:
        """Load payment records"""
        if self.payments_file.exists():
            try:
                with open(self.payments_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load payments: {e}")
                return []
        return []
    
    def _save_payments(self, payments: List[Dict[str, Any]]) -> bool:
        """Save payment records"""
        try:
            with open(self.payments_file, 'w') as f:
                json.dump(payments, f, indent=2)
            logging.info("Payment records saved")
            return True
        except Exception as e:
            logging.error(f"Failed to save payments: {e}")
            return False
    
    def get_payment_statistics(self) -> Dict[str, Any]:
        """Get payment statistics"""
        payments = self._load_payments()
        
        total_donated = sum(p.get('amount', 0) for p in payments if p.get('method') == 'paypal')
        
        paypal_payments = [p for p in payments if p.get('method') == 'paypal']
        
        stats = {
            'total_donated': total_donated,
            'total_transactions': len(payments),
            'paypal_transactions': len(paypal_payments),
            'monthly_donated': self._calculate_monthly_donations(payments),
            'average_donation': total_donated / len(paypal_payments) if paypal_payments else 0,
            'top_donor': self._get_top_donor(payments),
            'revenue_this_month': self._calculate_monthly_revenue(payments),
            'revenue_total': total_donated
        }
        
        return stats
    
    def _calculate_monthly_donations(self, payments: List[Dict[str, Any]]) -> float:
        """Calculate monthly donations"""
        current_month = datetime.now().strftime('%Y-%m')
        monthly_payments = [p for p in payments 
                         if p.get('created_at', '').startswith(current_month)]
        
        return sum(p.get('amount', 0) for p in monthly_payments)
    
    def _get_top_donor(self, payments: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get top donor"""
        if not payments:
            return None
        
        top_donor = max(payments, key=lambda p: p.get('amount', 0))
        
        return top_donor
    
    def _calculate_monthly_revenue(self, payments: List[Dict[str, Any]]) -> float:
        """Calculate monthly revenue"""
        current_month = datetime.now().strftime('%Y-%m')
        monthly_revenue = self._calculate_monthly_donations(payments)
        
        return monthly_revenue
    
    def handle_paypal_webhook(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle PayPal webhook notifications"""
        webhook_id = request_data.get('id')
        
        if webhook_id:
            payment_record = self._update_payment_status(webhook_id, request_data)
            
            if payment_record:
                return {
                    'success': True,
                    'message': f'Payment {webhook_id} processed',
                    'payment_info': payment_record
                }
        
        return {
            'success': False,
            'error': f'Webhook processing failed for ID: {webhook_id}'
        }
    
    def _update_payment_status(self, payment_id: str, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update payment status based on webhook data"""
        payments = self._load_payments()
        
        for payment in payments:
            if (payment.get('paypal_order_id') == payment_id or 
                payment.get('paypal_webhook_id') == payment_id):
                
                # Update payment status based on webhook event type
                event_type = webhook_data.get('event_type')
                
                if event_type == 'PAYMENT.AUTHORIZATION.CREATED':
                    payment['status'] = 'authorized'
                elif event_type == 'PAYMENT.AUTHORIZATION.VOIDED':
                    payment['status'] = 'voided'
                elif event_type == 'PAYMENT.CAPTURE.COMPLETED':
                    payment['status'] = 'completed'
                elif event_type == 'PAYMENT.CAPTURE.DENIED':
                    payment['status'] = 'denied'
                
                payment['updated_at'] = datetime.now().isoformat()
                payment['webhook_data'] = webhook_data
                
                self._save_payments(payments)
                return payment
        
        return None
    
    def generate_donation_buttons(self, container_widget) -> List[Any]:
        """Generate donation buttons for GUI"""
        if not self.paypal_config['client_id']:
            return []
        
        amounts = [5, 10, 20, 50, 100]
        button_data = []
        
        for amount in amounts:
            btn_data = {
                'amount': amount,
                'description': f'Donate ${amount}',
                'order_response': self.create_paypal_order(amount, f'Terry donation ${amount}'),
                'on_click': f"process_paypal_donation({amount})"
            }
            button_data.append(btn_data)
        
        return button_data
    
    def get_cashapp_integration_code(self, app_id: str = None) -> str:
        """Get Cash App integration code for specific user"""
        # This would integrate with Cash App APIs
        # For now, return a placeholder URL
        cashapp_url = f"https://cash.app/$app_id" if app_id else "https://cash.app/$CASH_TAG"
        
        return f"""
        <div style="font-family: Arial, sans-serif; font-size: 14px;">
            <p>Click here to donate via Cash App:</p>
            <a href="{cashapp_url}" target="_blank">
                <button style="background: #00D4AA; color: white; padding: 8px 12px; border: none; border-radius: 4px; font-weight: bold;">
                    📱 Open Cash App
                </button>
            </a>
            <p style="margin-top: 10px; color: #666; font-size: 12px;">$5 minimum donation appreciated!</p>
        </div>
        """
    
    def process_donation(self, amount: float, method: str = 'paypal', 
                        custom_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process donation in real-time"""
        if method == 'paypal':
            return self._process_paypal_donation(amount, custom_data)
        elif method == 'cashapp':
            return self._process_cashapp_donation(amount, custom_data)
        else:
            return {
                'success': False,
                'error': f'Unsupported donation method: {method}'
            }
    
    def _process_paypal_donation(self, amount: float, custom_data: Optional[Dict[str, Any]] = Dict[str, Any]:
        """Process PayPal donation"""
        try:
            # Create PayPal order
            order_result = self.create_paypal_order(
                amount,
                f"Support Terry-the-Tool-Bot Development - ${amount} donation",
                custom_data.get('custom_id') if custom_data else None
            )
            
            if order_result['success']:
                payment_info = order_result.get('payment_info')
                
                return {
                    'success': True,
                    'message': 'Donation initiated successfully',
                    'payment_info': payment_info,
                    'approval_url': order_result.get('approval_url'),
                    'amount': amount
                    'currency': self.paypal_config['currency']
                }
            else:
                return order_result
                
        except Exception as e:
            return {
                'success': False,
                'error': f'PayPal donation processing failed: {str(e)}'
            }
    
    def _process_cashapp_donation(self, amount: float, custom_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process Cash App donation"""
        # This would integrate with Cash App APIs
        # For now, return a pending status
        return {
            'success': True,
            'message': 'Cash App donation processing',
            'cashapp_url': self.get_cashapp_integration_code(custom_data.get('cashapp_tag') if custom_data else None),
            'amount': amount,
            'currency': 'USD',
            'status': 'pending'
        }
    
    def get_payment_summary(self) -> Dict[str, Any]:
        """Get payment summary for GUI display"""
        stats = self.get_payment_statistics()
        
        return {
            'total_donated': stats['total_donated'],
            'paypal_transactions': stats['paypal_transactions'],
            'monthly_average': stats['average_donation'],
            'top_donor': stats['top_donor'],
            'monthly_revenue': stats['revenue_this_month'],
            'paypal_configured': bool(self.paypal_config['client_id']),
            'cashapp_configured': False  # Would check for Cash App config
        }
    
    def configure_paypal(self, client_id: str, client_secret: str, 
                        sandbox_mode: bool = False) -> Dict[str, Any]:
        """Configure PayPal integration"""
        config = {
            'client_id': client_id,
            'client_secret': client_secret,
            'sandbox_mode': sandbox_mode,
            'last_updated': datetime.now().isoformat()
        }
        
        if self._save_paypal_config(config):
            self.paypal_config.update(config)
            return {
                'success': True,
                'message': 'PayPal configuration updated'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to save PayPal configuration'
            }
    
    def get_recent_donations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent donation records"""
        payments = self._load_payments()
        
        # Sort by created date (newest first)
        sorted_payments = sorted(payments, 
                               key=lambda p: p.get('created_at', ''), 
                               reverse=True)
        
        return sorted_payments[:limit]
    
    def export_payment_data(self) -> str:
        """Export payment data for accounting"""
        payments = self._load_payments()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_donations': sum(p.get('amount', 0) for p in payments),
            'paypal_transactions': len([p for p in payments if p.get('method') == 'paypal']),
            'monthly_revenue': self._calculate_monthly_revenue(payments),
            'payments_by_month': self._group_payments_by_month(payments)
        }
        
        return json.dumps(export_data, indent=2)