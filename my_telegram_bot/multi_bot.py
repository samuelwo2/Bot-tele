import json
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

class TelegramBot:
    def __init__(self, config: dict):
        self.config = config
        self.app = Application.builder().token(config["token"]).build()
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("custom", self.custom_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))  # Thêm handler cho nút bấm

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        photo_url = self.config.get('welcome_image_url', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR708VjiHtGT2oo52fIzvXS44x39lXuj7LRKA&s')
        await update.message.reply_photo(
            photo=photo_url,

    )
        # Tạo bàn phím với các nút
        keyboard = [
            [
                InlineKeyboardButton("Nhận khuyến mãi", callback_data='giftcode'),
            ],
            [
                InlineKeyboardButton("Tham gia kênh", url=self.config.get('channel_link', '')),
            ],
            [
                InlineKeyboardButton("Liên hệ Admin", url=f"https://t.me/{self.config['admin_contact']}")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Xin mừng đến nhóm {self.config.get('username', '')}\n"
            f"Liên hệ ADMIN KÈO: @{self.config['admin_contact']}\n"
            f"Nhận khuyến mãi LH @{self.config['admin_contact']}!",
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Liên hệ @{self.config['admin_contact']} để được hỗ trợ")

    async def custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Vào nhóm @{self.config.get('channel_link', '')} để nhận thông tin mới nhất.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.lower()
        if 'xin link' in text:
            await update.message.reply_text(f"Link đăng ký: {self.config['registration_link']}")
        if 'giftcode' in text:
            await update.message.reply_text(f"Bạn đã nhận được giftcode: {self.config.get('giftcode', 'XXXX-XXXX-XXXX')}")    
        else:
            await update.message.reply_text(f"Liên hệ @{self.config['admin_contact']} để biết thêm chi tiết")

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        # Xử lý khi người dùng nhấn vào các nút
        if query.data == 'giftcode':
            await query.edit_message_text(text=f"Bạn đã nhận được giftcode: {self.config.get('giftcode', 'XXXX-XXXX-XXXX')}")
        elif query.data == 'Tham gia kênh':
            await query.edit_message_text(text=f"Link chia sẻ: {self.config['channel_link']}")
        elif query.data == 'Liên hệ Admin':
            await query.edit_message_text(text=f"Tải app tại: {self.config.get('admin_contact', '')}")

    async def run(self):
        print(f"🚀 Đang khởi chạy bot @{self.config['username']}...")
        await self.app.initialize()
        await self.app.start()
        try:
            await self.app.updater.start_polling()
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            await self.app.stop()
            await self.app.shutdown()

async def main():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        bots = [TelegramBot(bot_config) for bot_config in config["bots"]]
        tasks = [asyncio.create_task(bot.run()) for bot in bots]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng bot...")
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("✅ Đã dừng bot an toàn")