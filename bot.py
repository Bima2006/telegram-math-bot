import openai
import pytesseract
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from PIL import Image
from sympy import symbols, Eq, solve

# Replace with your token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# OpenAI API Key (For future enhancements)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Bot setup
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
bot = Bot(TOKEN)

# Command to start the bot
def start(update, context):
    update.message.reply_text("Hi! I am your Math Solver Bot. Send me a photo of a math problem!")

# Handle photos (OCR part)
def handle_photo(update, context):
    photo = update.message.photo[-1]
    file = photo.get_file()
    file.download('math_problem.jpg')

    problem = extract_math_from_image('math_problem.jpg')
    solution = solve_math_problem(problem)

    update.message.reply_text(f"📊 Math Problem: {problem}\n\n{solution}")

def extract_math_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text.strip()

def solve_math_problem(problem):
    try:
        x = symbols('x')
        equation = Eq(eval(problem.split("=")[0]), eval(problem.split("=")[1]))
        solution = solve(equation, x)
        return f"📌 Answer: x = {solution}"
    except:
        return "🤖 AI couldn't solve this equation."

# Add handlers
start_handler = CommandHandler('start', start)
photo_handler = MessageHandler(Filters.photo, handle_photo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(photo_handler)

# Start bot
updater.start_polling()
