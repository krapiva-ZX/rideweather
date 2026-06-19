from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

TOKEN = "8822660751:AAHBHH2_S8r22nnAF6xQjtKt9TZENbl7w0M"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "RideWeather жив 🏍️🌦️\n\n"
        "Пример:\n"
        "/weather Moscow"
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Использование:\n/weather Moscow"
        )
        return

    city = " ".join(context.args)

    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        ).json()

        if "results" not in geo:
            await update.message.reply_text("Город не найден")
            return

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]
        city_name = geo["results"][0]["name"]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m"
            }
        ).json()

        temp = weather["current"]["temperature_2m"]
        wind = weather["current"]["wind_speed_10m"]

        advice = []

        if temp < 10:
            advice.append("🧥 Тёплая куртка")

        elif temp < 20:
            advice.append("🏍️ Мотокуртка")

        else:
            advice.append("👕 Лёгкая экипировка")

        if wind > 25:
            advice.append("💨 Сильный ветер")

        text = (
            f"🏍 {city_name}\n\n"
            f"🌡 Температура: {temp}°C\n"
            f"💨 Ветер: {wind} км/ч\n\n"
            f"Рекомендации:\n"
            + "\n".join(advice)
        )

        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    print("BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()