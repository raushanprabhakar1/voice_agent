"""
Database operations using Supabase
"""
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        self._ensure_tables()

    def _ensure_tables(self):
        """Ensure database tables exist (run migrations if needed)"""
        # Note: In production, you'd use Supabase migrations
        # For now, we'll assume tables are created via Supabase dashboard
        pass

    async def get_user_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """Get user by phone number"""
        try:
            result = self.client.table("users").select("*").eq("phone", phone).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def create_user(self, phone: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Create a new user"""
        try:
            result = self.client.table("users").insert({
                "phone": phone,
                "name": name,
                "created_at": datetime.now().isoformat(),
            }).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error creating user: {e}")
            # If user already exists, return existing user
            return await self.get_user_by_phone(phone) or {}

    async def get_available_slots(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get available appointment slots - only returns slots that are NOT already booked"""
        # Hardcoded slot times: 9 AM, 11 AM, 2 PM, 4 PM
        slot_times = ["09:00", "11:00", "14:00", "16:00"]
        
        base_date = datetime.now()
        if date:
            try:
                base_date = datetime.fromisoformat(date.replace("Z", "+00:00"))
            except:
                pass
        
        # Get all booked appointments (confirmed status only)
        try:
            booked_result = self.client.table("appointments").select(
                "appointment_datetime"
            ).eq("status", "confirmed").execute()
            
            # Create a set of booked datetimes for fast lookup
            booked_datetimes = set()
            for appointment in booked_result.data or []:
                booked_datetime = appointment.get("appointment_datetime")
                if booked_datetime:
                    # Normalize datetime format to match slot format: YYYY-MM-DDTHH:MM:00
                    # Handle various formats: "2024-01-01T09:00:00", "2024-01-01T09:00", etc.
                    if "T" in booked_datetime:
                        date_part, time_part = booked_datetime.split("T")
                        # Extract HH:MM from time part (ignore seconds/microseconds/timezone)
                        time_only = time_part.split(":")[:2]  # Get HH and MM
                        if len(time_only) == 2:
                            normalized_dt = f"{date_part}T{time_only[0].zfill(2)}:{time_only[1].zfill(2)}:00"
                            booked_datetimes.add(normalized_dt)
        except Exception as e:
            print(f"Error fetching booked appointments: {e}")
            booked_datetimes = set()
        
        # Generate all possible slots for next 7 days
        all_slots = []
        for day_offset in range(7):
            slot_date = base_date + timedelta(days=day_offset)
            date_str = slot_date.strftime("%Y-%m-%d")
            
            # Add slots: 9 AM, 11 AM, 2 PM, 4 PM
            for time_str in slot_times:
                datetime_str = f"{date_str}T{time_str}:00"
                all_slots.append({
                    "date": date_str,
                    "time": time_str,
                    "datetime": datetime_str,
                })
        
        # Filter out booked slots - only return available ones
        available_slots = [
            slot for slot in all_slots 
            if slot["datetime"] not in booked_datetimes
        ]
        
        return available_slots

    async def book_appointment(
        self,
        user_phone: str,
        date: str,
        time: str,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Book an appointment - only allows booking available slots"""
        try:
            # Normalize time format (ensure HH:MM format)
            if ":" not in time:
                raise ValueError("Invalid time format. Expected HH:MM")
            
            time_parts = time.split(":")
            if len(time_parts) != 2:
                raise ValueError("Invalid time format. Expected HH:MM")
            
            # Ensure time is in HH:MM format
            hour, minute = time_parts[0].zfill(2), time_parts[1].zfill(2)
            normalized_time = f"{hour}:{minute}"
            datetime_str = f"{date}T{normalized_time}:00"
            
            # Check if slot is already booked (double-check for race conditions)
            existing = self.client.table("appointments").select("*").eq(
                "appointment_datetime", datetime_str
            ).eq("status", "confirmed").execute()
            
            if existing.data:
                raise ValueError(f"Slot already booked for {date} at {normalized_time}")
            
            # Verify this is a valid slot time (9 AM, 11 AM, 2 PM, 4 PM)
            valid_times = ["09:00", "11:00", "14:00", "16:00"]
            if normalized_time not in valid_times:
                raise ValueError(f"Invalid time slot. Available times are: {', '.join(valid_times)}")
            
            # Create appointment
            result = self.client.table("appointments").insert({
                "user_phone": user_phone,
                "appointment_date": date,
                "appointment_time": normalized_time,
                "appointment_datetime": datetime_str,
                "status": "confirmed",
                "notes": notes,
                "created_at": datetime.now().isoformat(),
            }).execute()
            
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error booking appointment: {e}")
            raise

    async def get_user_appointments(
        self,
        user_phone: str,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get user's appointments"""
        try:
            query = self.client.table("appointments").select("*").eq("user_phone", user_phone)
            
            if status:
                query = query.eq("status", status)
            
            result = query.order("appointment_datetime", desc=True).execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return []

    async def cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """Cancel an appointment"""
        try:
            result = self.client.table("appointments").update({
                "status": "cancelled",
                "updated_at": datetime.now().isoformat(),
            }).eq("id", appointment_id).execute()
            
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error cancelling appointment: {e}")
            raise

    async def modify_appointment(
        self,
        appointment_id: str,
        date: Optional[str] = None,
        time: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Modify an appointment"""
        try:
            update_data = {"updated_at": datetime.now().isoformat()}
            
            if date:
                update_data["appointment_date"] = date
            if time:
                update_data["appointment_time"] = time
            if date or time:
                update_data["appointment_datetime"] = f"{date or ''}T{time or ''}:00"
            if notes is not None:
                update_data["notes"] = notes
            
            result = self.client.table("appointments").update(update_data).eq(
                "id", appointment_id
            ).execute()
            
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error modifying appointment: {e}")
            raise

    async def save_conversation_summary(
        self,
        user_phone: str,
        summary: Dict[str, Any],
        tool_calls: List[Dict[str, Any]],
    ):
        """Save conversation summary"""
        try:
            self.client.table("conversation_summaries").insert({
                "user_phone": user_phone,
                "summary": summary,
                "tool_calls": tool_calls,
                "created_at": datetime.now().isoformat(),
            }).execute()
        except Exception as e:
            print(f"Error saving summary: {e}")
