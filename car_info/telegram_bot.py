import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '6731003050:AAHbsfLVjMc6595RE3JylXK52r2u0nX18mk'
DJANGO_API_URL = 'http://django:8000/api/cars'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Это ваш бот. Вы можете использовать следующие команды:\n'
        '/list_cars - Список всех автомобилей\n'
        '/upload_file - Загрузить XML файл\n'
        '/clear_cars - Очистить все автомобили\n'
        '/get_car <id> - Получить автомобиль по ID'
    )

async def list_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get(f'{DJANGO_API_URL}/')
    if response.status_code == 200:
        cars = response.json()
        if cars:
            message = '\n'.join([f"{car['make']} {car['model']} ({car['year']}) - ${car['price']}" for car in cars])
        else:
            message = 'Автомобили отсутствуют.'
    else:
        message = 'Не удалось получить список автомобилей.'
    await update.message.reply_text(message)

async def upload_file_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Пожалуйста, прикрепите XML файл для загрузки.')

async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = update.message.document
    if file.mime_type == 'application/xml':
        file_info = await file.get_file()
        file_path = file_info.file_path
        file_data = requests.get(file_path).content
        response = requests.post(f'{DJANGO_API_URL}/upload_file/', files={'file': ('file.xml', file_data, 'application/xml')})
        if response.status_code == 200:
            message = 'Файл успешно загружен и автомобили распарсены.'
        else:
            message = 'Не удалось загрузить файл.'
    else:
        message = 'Неправильный формат файла. Пожалуйста, прикрепите XML файл.'
    await update.message.reply_text(message)

async def clear_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.delete(f'{DJANGO_API_URL}/clear/')
    if response.status_code == 200:
        message = 'Успешно очищено.'
    else:
        message = 'Не удалось очистить автомобили.'
    await update.message.reply_text(message)

async def get_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        car_id = context.args[0]
        response = requests.get(f'{DJANGO_API_URL}/{car_id}/')
        if response.status_code == 200:
            car = response.json()
            message = f"{car['make']} {car['model']} ({car['year']}) - ${car['price']}"
        else:
            message = 'Автомобиль не найден.'
    else:
        message = 'Пожалуйста, укажите ID автомобиля.'
    await update.message.reply_text(message)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('list_cars', list_cars))
    application.add_handler(CommandHandler('upload_file', upload_file_command))
    application.add_handler(CommandHandler('clear_cars', clear_cars))
    application.add_handler(CommandHandler('get_car', get_car))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file_upload))

    application.run_polling()

if __name__ == '__main__':
    main()
