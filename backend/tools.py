"""
Tool definitions and execution for the appointment agent
"""
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from livekit.agents import llm
from database import Database


class AppointmentTools:
    def __init__(self, db: Database):
        self.db = db
        self.user_phone = None

    def get_tool_definitions(self) -> List[llm.RawFunctionTool]:
        """Define all available tools"""
        # When using raw_schema, functions must accept raw_arguments: dict[str, object]
        # This is the format LiveKit expects for raw function tools
        async def identify_user(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            phone = raw_arguments.get("phone")
            if not phone:
                return {
                    "error": "Phone number is required",
                    "message": "Please ask the user for their phone number first, then call this tool again with the phone number they provide."
                }
            return await self._identify_user(str(phone))
        
        async def fetch_slots(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            date = raw_arguments.get("date")
            return await self._fetch_slots(str(date) if date else None)
        
        async def book_appointment(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            date = raw_arguments.get("date")
            time = raw_arguments.get("time")
            notes = raw_arguments.get("notes")
            return await self._book_appointment(
                str(date) if date else "",
                str(time) if time else "",
                str(notes) if notes else None
            )
        
        async def retrieve_appointments(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            status = raw_arguments.get("status")
            return await self._retrieve_appointments(str(status) if status else None)
        
        async def cancel_appointment(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            appointment_id = raw_arguments.get("appointment_id")
            if not appointment_id:
                return {"error": "Appointment ID is required"}
            return await self._cancel_appointment(str(appointment_id))
        
        async def modify_appointment(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            appointment_id = raw_arguments.get("appointment_id")
            if not appointment_id:
                return {"error": "Appointment ID is required"}
            date = raw_arguments.get("date")
            time = raw_arguments.get("time")
            notes = raw_arguments.get("notes")
            return await self._modify_appointment(
                str(appointment_id),
                str(date) if date else None,
                str(time) if time else None,
                str(notes) if notes else None
            )
        
        async def end_conversation(raw_arguments: dict[str, object]) -> Dict[str, Any]:
            return await self._end_conversation()
        
        return [
            llm.function_tool(
                identify_user,
                raw_schema={
                    "name": "identify_user",
                    "description": "Ask for and store user's phone number to identify them. Use this first before booking appointments.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "phone": {
                                "type": "string",
                                "description": "User's phone number (e.g., +1234567890). IMPORTANT: You must first ask the user for their phone number in conversation, wait for their response, then call this tool with the phone number they provide. Do not call this tool without a phone number.",
                            },
                        },
                        "required": ["phone"],
                    },
                },
            ),
            llm.function_tool(
                fetch_slots,
                raw_schema={
                    "name": "fetch_slots",
                    "description": "Fetch available appointment slots. Returns ONLY slots that are not already booked. Slots are available at 9 AM, 11 AM, 2 PM, and 4 PM for the next 7 days. When booking, you can book the first available slot from the results.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Optional date to fetch slots for (YYYY-MM-DD). If not provided, returns available slots for next 7 days.",
                            },
                        },
                    },
                },
            ),
            llm.function_tool(
                book_appointment,
                raw_schema={
                    "name": "book_appointment",
                    "description": "Book an appointment for the user. Requires user to be identified first. IMPORTANT: Only book slots that were returned by fetch_slots - those are guaranteed to be available. When user wants to book, first call fetch_slots to get available slots, then book the first available slot from the results.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "Appointment date in YYYY-MM-DD format. Must be from available slots returned by fetch_slots.",
                            },
                            "time": {
                                "type": "string",
                                "description": "Appointment time in HH:MM format (24-hour). Must be from available slots returned by fetch_slots (09:00, 11:00, 14:00, or 16:00).",
                            },
                            "notes": {
                                "type": "string",
                                "description": "Optional notes about the appointment",
                            },
                        },
                        "required": ["date", "time"],
                    },
                },
            ),
            llm.function_tool(
                retrieve_appointments,
                raw_schema={
                    "name": "retrieve_appointments",
                    "description": "Retrieve all appointments for the identified user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "description": "Optional filter by status: 'confirmed', 'cancelled', or None for all",
                                "enum": ["confirmed", "cancelled", None],
                            },
                        },
                    },
                },
            ),
            llm.function_tool(
                cancel_appointment,
                raw_schema={
                    "name": "cancel_appointment",
                    "description": "Cancel a specific appointment by ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "string",
                                "description": "The ID of the appointment to cancel",
                            },
                        },
                        "required": ["appointment_id"],
                    },
                },
            ),
            llm.function_tool(
                modify_appointment,
                raw_schema={
                    "name": "modify_appointment",
                    "description": "Modify an existing appointment's date, time, or notes.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "string",
                                "description": "The ID of the appointment to modify",
                            },
                            "date": {
                                "type": "string",
                                "description": "New appointment date in YYYY-MM-DD format",
                            },
                            "time": {
                                "type": "string",
                                "description": "New appointment time in HH:MM format (24-hour)",
                            },
                            "notes": {
                                "type": "string",
                                "description": "Updated notes for the appointment",
                            },
                        },
                        "required": ["appointment_id"],
                    },
                },
            ),
            llm.function_tool(
                end_conversation,
                raw_schema={
                    "name": "end_conversation",
                    "description": "End the conversation and generate a summary. Use this when the user wants to end the call.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            ),
        ]

    async def execute_tool(self, tool_call: llm.FunctionToolCall) -> Dict[str, Any]:
        """Execute a tool call"""
        function_name = tool_call.name
        args = json.loads(tool_call.arguments) if isinstance(
            tool_call.arguments, str
        ) else tool_call.arguments

        try:
            if function_name == "identify_user":
                return await self._identify_user(args.get("phone"))
            elif function_name == "fetch_slots":
                return await self._fetch_slots(args.get("date"))
            elif function_name == "book_appointment":
                return await self._book_appointment(
                    args.get("date"),
                    args.get("time"),
                    args.get("notes"),
                )
            elif function_name == "retrieve_appointments":
                return await self._retrieve_appointments(args.get("status"))
            elif function_name == "cancel_appointment":
                return await self._cancel_appointment(args.get("appointment_id"))
            elif function_name == "modify_appointment":
                return await self._modify_appointment(
                    args.get("appointment_id"),
                    args.get("date"),
                    args.get("time"),
                    args.get("notes"),
                )
            elif function_name == "end_conversation":
                return await self._end_conversation()
            else:
                return {"error": f"Unknown tool: {function_name}"}
        except Exception as e:
            return {"error": str(e), "tool": function_name}

    async def _identify_user(self, phone: str) -> Dict[str, Any]:
        """Identify user by phone number"""
        if not phone:
            return {"error": "Phone number is required"}
        
        self.user_phone = phone
        user = await self.db.get_user_by_phone(phone)
        
        if not user:
            user = await self.db.create_user(phone)
        
        return {
            "success": True,
            "user": {
                "phone": user.get("phone", phone),
                "name": user.get("name"),
            },
            "message": f"User identified: {phone}",
        }

    async def _fetch_slots(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Fetch available appointment slots"""
        slots = await self.db.get_available_slots(date)
        return {
            "success": True,
            "slots": slots,
            "count": len(slots),
        }

    async def _book_appointment(
        self,
        date: str,
        time: str,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Book an appointment"""
        if not self.user_phone:
            return {
                "error": "User must be identified first. Please use identify_user tool.",
            }
        
        if not date or not time:
            return {"error": "Date and time are required"}
        
        try:
            appointment = await self.db.book_appointment(
                user_phone=self.user_phone,
                date=date,
                time=time,
                notes=notes,
            )
            return {
                "success": True,
                "appointment": appointment,
                "message": f"Appointment booked for {date} at {time}",
            }
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Failed to book appointment: {str(e)}"}

    async def _retrieve_appointments(self, status: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve user's appointments"""
        if not self.user_phone:
            return {
                "error": "User must be identified first. Please use identify_user tool.",
            }
        
        appointments = await self.db.get_user_appointments(
            user_phone=self.user_phone,
            status=status,
        )
        return {
            "success": True,
            "appointments": appointments,
            "count": len(appointments),
        }

    async def _cancel_appointment(self, appointment_id: str) -> Dict[str, Any]:
        """Cancel an appointment"""
        if not appointment_id:
            return {"error": "Appointment ID is required"}
        
        try:
            appointment = await self.db.cancel_appointment(appointment_id)
            return {
                "success": True,
                "appointment": appointment,
                "message": "Appointment cancelled successfully",
            }
        except Exception as e:
            return {"error": f"Failed to cancel appointment: {str(e)}"}

    async def _modify_appointment(
        self,
        appointment_id: str,
        date: Optional[str] = None,
        time: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Modify an appointment"""
        if not appointment_id:
            return {"error": "Appointment ID is required"}
        
        try:
            appointment = await self.db.modify_appointment(
                appointment_id=appointment_id,
                date=date,
                time=time,
                notes=notes,
            )
            return {
                "success": True,
                "appointment": appointment,
                "message": "Appointment modified successfully",
            }
        except Exception as e:
            return {"error": f"Failed to modify appointment: {str(e)}"}

    async def _end_conversation(self) -> Dict[str, Any]:
        """End conversation"""
        return {
            "success": True,
            "message": "Conversation ending. Summary will be generated.",
        }
