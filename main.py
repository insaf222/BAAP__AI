# 🛑 Block all discord voice features safely to avoid 'audioop' errors
import sys
import types

# Custom dummy VoiceClient with expected attributes
class DummyVoiceClient:
    warn_nacl = False  # Required by discord.client
    def __init__(self, *args, **kwargs):
        pass

class DummyVoiceProtocol:
    def __init__(self, *args, **kwargs):
        pass

# Patch the modules
voice_client_patch = types.ModuleType("discord.voice_client")
voice_client_patch.VoiceClient = DummyVoiceClient
voice_client_patch.VoiceProtocol = DummyVoiceProtocol

sys.modules["audioop"] = types.ModuleType("audioop")
sys.modules["discord.voice_client"] = voice_client_patch
sys.modules["discord.player"] = types.ModuleType("discord.player")
import discord
from discord.ext import commands
import google.generativeai as genai
import os
import random
import asyncio

# Gemini Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🔥 Baap AI is Online as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="DM + Mention Roast 🔥"))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        try:
            prompt = f"You are Baap AI. Someone DMed: '{message.content}'. Roast them in funny, abusive Haryanvi style."
            response = model.generate_content(prompt)
            await message.channel.send(response.text.strip())
        except Exception as e:
            await message.channel.send("Gemini bekaar ho gaya bhai 😵‍💫")
            print(e)
        return

    if message.mentions:
        for target in message.mentions:
            if not target.bot:
                await message.channel.send(f"{target.mention} ab 20 second ka timeout! 😈")
                try:
                    def check(m): return m.author.id == target.id and m.channel.id == message.channel.id
                    await bot.wait_for("message", timeout=20, check=check)
                    await message.channel.send(f"{target.mention} ne reply diya, bach gaya! 😅")
                except asyncio.TimeoutError:
                    roast1 = model.generate_content(f"Roast {message.author.display_name} in street Haryanvi").text.strip()
                    roast2 = model.generate_content(f"Roast {target.display_name} in street Haryanvi").text.strip()
                    await message.channel.send(roast1)
                    await message.channel.send(roast2)

bot.run(os.getenv("DISCORD_TOKEN"))
