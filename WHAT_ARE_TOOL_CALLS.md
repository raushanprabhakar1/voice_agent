# 🔧 What Are Tool Calls?

## Simple Explanation

**Tool calls** are actions the AI agent performs to help you. Think of them as the agent's "hands" - ways it can interact with the system to do things for you.

## Real-World Analogy

Imagine you're talking to a human assistant:

- **You say**: "I want to book an appointment for tomorrow at 2 PM"
- **Assistant thinks**: "I need to:
  1. Check who you are (identify_user)
  2. Check if 2 PM tomorrow is available (fetch_slots)
  3. Book the appointment (book_appointment)"

Each of these steps is a **tool call** - the assistant uses "tools" to complete your request.

## In This System

### What Happens:

1. **You speak**: "I want to book an appointment"
2. **AI listens**: Converts your speech to text
3. **AI thinks**: "The user wants to book an appointment. I need to:
   - First identify the user (get their phone number)
   - Then check available slots
   - Then book the appointment"
4. **AI uses tools**: Calls functions like `identify_user()`, `fetch_slots()`, `book_appointment()`
5. **Tools execute**: Each tool does its job (saves to database, checks availability, etc.)
6. **AI responds**: "I've booked your appointment for tomorrow at 2 PM"

### The 7 Tools Available:

1. **`identify_user`** 👤
   - **What it does**: Asks for and stores your phone number
   - **Example**: "What's your phone number?" → Stores it

2. **`fetch_slots`** 📅
   - **What it does**: Gets available appointment times
   - **Example**: "What times are available tomorrow?" → Returns list of slots

3. **`book_appointment`** ✅
   - **What it does**: Books an appointment in the database
   - **Example**: "Book me for tomorrow at 2 PM" → Creates appointment record

4. **`retrieve_appointments`** 📋
   - **What it does**: Gets your past/upcoming appointments
   - **Example**: "Show me my appointments" → Returns your appointment list

5. **`cancel_appointment`** ❌
   - **What it does**: Cancels a specific appointment
   - **Example**: "Cancel my appointment on Friday" → Marks it as cancelled

6. **`modify_appointment`** ✏️
   - **What it does**: Changes appointment date/time
   - **Example**: "Move my appointment to next week" → Updates the appointment

7. **`end_conversation`** 👋
   - **What it does**: Ends the call and generates summary
   - **Example**: "Goodbye" → Ends call, creates summary

## Why Tool Calls Matter

### Without Tool Calls:
- AI can only talk - it can't actually do anything
- It can't save data, check databases, or perform actions
- It's just a chatbot

### With Tool Calls:
- AI can actually **do things** for you
- It can save appointments, check availability, modify records
- It's a **functional assistant** that can complete tasks

## How It Works Technically

### 1. LLM Decides to Use a Tool

When you say "I want to book an appointment", the LLM (AI brain) thinks:
```
User wants to book appointment
→ I need to call book_appointment tool
→ But first, I need the user's phone number
→ So I should call identify_user first
```

### 2. Tool Gets Called

The LLM sends a request like:
```json
{
  "name": "identify_user",
  "arguments": {
    "phone": "+1234567890"
  }
}
```

### 3. Tool Executes

The backend runs the `identify_user` function:
- Saves phone number to database
- Returns success message

### 4. LLM Gets Result

The tool returns:
```json
{
  "success": true,
  "user": {
    "phone": "+1234567890"
  }
}
```

### 5. LLM Responds

The LLM uses the result to respond:
- "Great! I've identified you. Now, when would you like to book?"

## Visual Example

**Conversation Flow:**

```
You: "I want to book an appointment for tomorrow at 2 PM"

AI: [Thinking...]
    → Tool Call: identify_user(phone="+1234567890")
    → Result: User identified
    → Tool Call: fetch_slots(date="2026-02-04")
    → Result: Available slots: 9 AM, 11 AM, 2 PM, 4 PM
    → Tool Call: book_appointment(date="2026-02-04", time="14:00")
    → Result: Appointment booked successfully

AI: "Perfect! I've booked your appointment for tomorrow at 2 PM. 
     Your appointment ID is #12345."
```

## In the UI

When a tool is called, you see:

```
🔧 Tool Calls
1 call

✅ Book Appointment
   Status: ✅ Success
   Arguments: { "date": "2026-02-04", "time": "14:00" }
   Result: { "success": true, "appointment": {...} }
```

This shows you:
- **What tool was used** (Book Appointment)
- **What information was sent** (date and time)
- **What happened** (success or error)
- **The result** (appointment details)

## Why You See "0 calls"

If you see "0 calls", it means:
- The AI hasn't used any tools yet
- You might need to ask it to do something that requires a tool
- Or the tool calls aren't being displayed (which we're fixing)

## Summary

**Tool calls = Actions the AI takes to help you**

- They're like buttons the AI can press
- Each tool does a specific job
- The AI decides when to use them
- You see them in the UI so you know what's happening
- They make the AI actually functional, not just talkative

Think of it like this:
- **Without tools**: AI is a chatbot that can only talk
- **With tools**: AI is an assistant that can actually do things for you
