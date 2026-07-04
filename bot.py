#!/usr/bin/env python3
"""
Telegram Bot для обработки APK файлов с встраиванием таблицы подписки
Admin-only bot with APK processing functionality
"""

import os
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, 
    filters, ContextTypes
)

from apk_processor import APKProcessor
from config import config

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for conversation
ADMIN_MENU, WAITING_FILES, WAITING_SINGLE_FILE, WAITING_LINK, WAITING_TITLE = range(5)

class APKBot:
    def __init__(self):
        self.processor = APKProcessor()
        self.admin_ids = config.ADMIN_IDS
        self.user_sessions = {}
        
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in self.admin_ids
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start command - show admin panel or deny access"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text(
                "❌ Access Denied\nЭтот бот доступен только администраторам."
            )
            return ConversationHandler.END
        
        keyboard = [
            ["📁 Загрузить файлы", "📄 Загрузить файл"],
            ["⚙️ Настройки", "❌ Выход"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "👤 Добро пожаловать в Admin Panel\n\n"
            "Выберите действие:",
            reply_markup=reply_markup
        )
        
        return ADMIN_MENU
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle admin menu selection"""
        user_id = update.effective_user.id
        text = update.message.text
        
        if text == "📁 Загрузить файлы":
            await update.message.reply_text(
                "📁 Режим массовой загрузки активирован\n\n"
                "Отправьте APK файлы (можно несколько):",
                reply_markup=ReplyKeyboardRemove()
            )
            self.user_sessions[user_id] = {
                'mode': 'multiple',
                'files': [],
                'title': config.DEFAULT_TITLE,
                'branding': config.DEFAULT_BRANDING
            }
            return WAITING_FILES
            
        elif text == "📄 Загрузить файл":
            await update.message.reply_text(
                "📄 Режим одиночной загрузки активирован\n\n"
                "Отправьте APK файл:",
                reply_markup=ReplyKeyboardRemove()
            )
            self.user_sessions[user_id] = {
                'mode': 'single',
                'files': [],
                'title': config.DEFAULT_TITLE,
                'branding': config.DEFAULT_BRANDING
            }
            return WAITING_SINGLE_FILE
            
        elif text == "⚙️ Настройки":
            await update.message.reply_text(
                "⚙️ Настройки по умолчанию:\n\n"
                f"Брендинг: {config.DEFAULT_BRANDING}\n"
                f"Заголовок: {config.DEFAULT_TITLE}\n\n"
                "Возврат в меню...",
                reply_markup=ReplyKeyboardMarkup([["◀️ Назад"]], resize_keyboard=True)
            )
            return ADMIN_MENU
            
        elif text == "❌ Выход" or text == "◀️ Назад":
            await update.message.reply_text(
                "До встречи! 👋",
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        
        return ADMIN_MENU
    
    async def handle_multiple_files(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle multiple file uploads"""
        user_id = update.effective_user.id
        
        if update.message.document:
            file = update.message.document
            file_path = await self._download_file(context, file)
            
            self.user_sessions[user_id]['files'].append(file_path)
            
            await update.message.reply_text(
                f"✅ Файл загружен: {file.file_name}\n\n"
                f"Всего файлов: {len(self.user_sessions[user_id]['files'])}\n\n"
                "Отправьте еще файлы или нажмите 'Готово':",
                reply_markup=ReplyKeyboardMarkup([["✅ Готово"]], resize_keyboard=True)
            )
            return WAITING_FILES
        
        elif update.message.text == "✅ Готово":
            if not self.user_sessions[user_id]['files']:
                await update.message.reply_text("❌ Нет файлов для обработки!")
                return WAITING_FILES
            
            await update.message.reply_text(
                "🔗 Отправьте ссылку на кнопку подписаться:",
                reply_markup=ReplyKeyboardRemove()
            )
            return WAITING_LINK
        
        return WAITING_FILES
    
    async def handle_single_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle single file upload"""
        user_id = update.effective_user.id
        
        if update.message.document:
            file = update.message.document
            file_path = await self._download_file(context, file)
            
            self.user_sessions[user_id]['files'].append(file_path)
            
            await update.message.reply_text(
                f"✅ Файл загружен: {file.file_name}\n\n"
                "🔗 Отправьте ссылку на кнопку подписаться:",
                reply_markup=ReplyKeyboardRemove()
            )
            return WAITING_LINK
        
        return WAITING_SINGLE_FILE
    
    async def handle_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle subscription link"""
        user_id = update.effective_user.id
        link = update.message.text.strip()
        
        if not link.startswith(('http://', 'https://', 't.me/', '@')):
            await update.message.reply_text("❌ Некорректная ссылка!\n\nПопробуйте еще раз:")
            return WAITING_LINK
        
        self.user_sessions[user_id]['link'] = link
        
        await update.message.reply_text(
            "📝 Укажите заголовок для таблицы (или нажмите 'Пропустить' для стандартного):",
            reply_markup=ReplyKeyboardMarkup([["⏭️ Пропустить"]], resize_keyboard=True)
        )
        
        return WAITING_TITLE
    
    async def handle_title(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle custom title"""
        user_id = update.effective_user.id
        
        if update.message.text != "⏭️ Пропустить":
            self.user_sessions[user_id]['title'] = update.message.text.strip()
        
        # Start processing
        await self._process_apks(update, user_id)
        
        return ConversationHandler.END
    
    async def _download_file(self, context: ContextTypes.DEFAULT_TYPE, file_obj) -> str:
        """Download file from Telegram"""
        file = await context.bot.get_file(file_obj.file_id)
        file_path = Path(config.WORK_DIR) / file_obj.file_name
        await file.download_to_drive(file_path)
        return str(file_path)
    
    async def _process_apks(self, update: Update, user_id: int):
        """Process APK files asynchronously"""
        session = self.user_sessions[user_id]
        files = session['files']
        link = session['link']
        title = session['title']
        branding = session['branding']
        
        processing_msg = await update.message.reply_text(
            "⏳ Обработка файлов...\n"
            "Это может занять несколько минут...",
            reply_markup=ReplyKeyboardRemove()
        )
        
        processed_files = []
        errors = []
        
        for file_path in files:
            try:
                logger.info(f"Processing {file_path}")
                output_path = await self.processor.process_apk(
                    input_path=file_path,
                    subscription_link=link,
                    title=title,
                    branding=branding
                )
                processed_files.append(output_path)
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                errors.append(f"❌ {Path(file_path).name}: {str(e)}")
        
        # Send results
        if processed_files:
            await update.message.reply_text("✅ Готово! Отправляю файлы...")
            for output_path in processed_files:
                try:
                    with open(output_path, 'rb') as f:
                        await update.message.reply_document(
                            document=f,
                            caption=f"✅ {Path(output_path).name}",
                        )
                except Exception as e:
                    logger.error(f"Error sending file {output_path}: {e}")
                    errors.append(f"❌ Ошибка отправки {Path(output_path).name}")
        
        if errors:
            await update.message.reply_text(
                "⚠️ Ошибки при обработке:\n\n" + "\n".join(errors)
            )
        
        try:
            await processing_msg.delete()
        except:
            pass
        
        # Show main menu button
        keyboard = [["📋 Главное меню"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Что дальше?",
            reply_markup=reply_markup
        )
        
        # Cleanup
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel operation"""
        user_id = update.effective_user.id
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        
        await update.message.reply_text(
            "❌ Операция отменена.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END


def main():
    """Start the bot"""
    load_dotenv()
    
    # Validate configuration
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN is not set. Please check your .env file")
        return
    
    if not config.ADMIN_IDS:
        logger.error("❌ ADMIN_IDS is not set. Please check your .env file")
        return
    
    # Create necessary directories
    Path(config.WORK_DIR).mkdir(parents=True, exist_ok=True)
    Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    logger.info("🚀 Starting APK Bot...")
    logger.info(f"Admin IDs: {config.ADMIN_IDS}")
    logger.info(f"Default branding: {config.DEFAULT_BRANDING}")
    
    # Initialize bot
    bot = APKBot()
    
    # Create application
    app = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot.start)],
        states={
            ADMIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot.admin_menu)
            ],
            WAITING_FILES: [
                MessageHandler(filters.Document.ALL, bot.handle_multiple_files),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_multiple_files)
            ],
            WAITING_SINGLE_FILE: [
                MessageHandler(filters.Document.ALL, bot.handle_single_file)
            ],
            WAITING_LINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_link)
            ],
            WAITING_TITLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_title)
            ],
        },
        fallbacks=[CommandHandler("cancel", bot.cancel)]
    )
    
    app.add_handler(conv_handler)
    
    logger.info("✅ Bot started! Waiting for commands...")
    app.run_polling()


if __name__ == "__main__":
    main()
