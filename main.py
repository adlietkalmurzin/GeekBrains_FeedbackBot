from interface.database.create_db import create_db
from aiogram import executor
from my_bot import dp


async def main(dp) -> None:
    create_db()
    bool(1)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=main, skip_updates=True)
