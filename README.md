# Telegram Bot — Why Not Manicure

## Short Description

This project is a **Telegram bot built with aiogram**, designed for initial communication with beauty salon clients.  
The bot automatically greets new users, collects contact information, and transfers the conversation to an administrator.

---

## Core Functionality

### Client Side
- Welcome message and short salon presentation
- Check whether the user is new
- Collects:
  - selected services
  - name and phone number
- Sends client data to administrators
- Enables further communication via the bot

### Admin Side
- `/users` command to download the client database
- Communication with clients via replies in a group chat
- Conversation termination using `/end`

---

## Dialogue Logic

A simple in-memory state system is used:
- `state 1` — service selection  
- `state 2` — contact details input  
- `state 3` — communication with administrator  

---

## Database

- **SQLite**
- Automatically created on startup
- Stores:
  - Telegram ID
  - username
  - full name
  - contact information
  - creation date

---

## Project Structure

- `main.py` — bot entry point
- `client.py` — client interaction logic
- `admin.py` — admin commands
- `db_handler.py` — SQLite database handling

---

## Purpose

This project demonstrates:
- a business-oriented Telegram bot
- lead collection workflow
- simple FSM logic without external storage
- aiogram + SQLite integration
