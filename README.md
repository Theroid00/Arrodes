---
title: Arrodes
emoji: 🔮
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Arrodes 

[![Invite Bot](https://img.shields.io/badge/Discord-Invite%20Bot-5865F2?logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1189633573611913328)
[![Discord Invite](https://img.shields.io/badge/Discord-Join%20Server-5865F2?logo=discord&logoColor=white)](https://discord.gg/YOUR_INVITE_LINK)
[![Status](https://img.shields.io/badge/Status-Active%20(VPS%2024%2F7)-success?logo=skynet&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1189633573611913328)

Arrodes is an advanced Discord bot built using the `disnake` library. Designed to streamline server management, boost community engagement, and offer dynamic features alongside seamless API integrations.

---

##  Uptime & Hosting
Arrodes is hosted on a dedicated **Virtual Private Server (VPS)** to ensure that it remains **active and online 24/7** with maximum reliability and auto-restart capability.

---

##  Invite & Support
Add Arrodes to your Discord server or join our support community:
-  **[Invite Arrodes to your server](https://discord.com/oauth2/authorize?client_id=1189633573611913328)**

---

##  Features
- **Custom Commands**: Configurable and easy-to-use commands for various functionalities.
- **Interactive Events**: Engage server members with fun and useful activities.
- **API Integration**: Extends capabilities through external APIs.
- **Moderation Tools**: Efficient features for managing your server.

---

##  Requirements
- Python 3.8 or higher
- Libraries:
  - `disnake`
  - `beautifulsoup4`
  - `requests`
  - `nltk`
  - See `requirements.txt` for the full list.

---

##  Installation & Deployment

### Quick Setup (VPS Deployment)
Deploy Arrodes to a fresh Ubuntu VM with a single script:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Theroid00/Arrodes/main/setup.sh)
```

### Manual Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Theroid00/Arrodes.git
   cd Arrodes
   ```

2. **Create environment configuration:**
   Create a `.env` file in the root directory:
   ```env
   BOT_TOKEN=your_discord_bot_token
   ```

3. **Start the bot using Docker Compose:**
   ```bash
   docker-compose up --build -d
   ```
