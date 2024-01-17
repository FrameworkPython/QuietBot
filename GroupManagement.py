from rubpy import Client, types, utils
from rubpy.types import Updates

class Bot(Client):
    def __init__(self, name):
        super().__init__(name)
        self.silent_users = []

    async def handle_updates(self, update: Updates):
        if update.object_guid == 'your gap guid' and update.message.author_object_guid == 'owner guid':
            if not update.message.reply_to_message_id:
                return

            full_message = await self.get_messages_by_id(update.object_guid, [update.message.reply_to_message_id])
            user_guid = full_message.messages[0].author_object_guid

            if update.message.text == 'سکوت':
                if user_guid not in self.silent_users:
                    self.silent_users.append(user_guid)
                    await update.reply(f'کاربر {utils.Mention("کاربر", user_guid)} در لیست سکوت قرار گرفت')
                    print(f'User {user_guid} added to silent_users list. Current list: {self.silent_users}')

            elif update.message.text == 'حذف از لیست سکوت':
                if user_guid in self.silent_users:
                    self.silent_users.remove(user_guid)
                    await update.reply(f'کاربر {utils.Mention("کاربر", user_guid)} از لیست سکوت حذف شد')
                    print(f'User {user_guid} removed from silent_users list. Current list: {self.silent_users}')

            elif update.message.text == 'بن':
                await self.ban_group_member(update.object_guid, user_guid)
                await update.reply(f'کاربر {utils.Mention("کاربر", user_guid)} از گروه حذف شد')

            elif update.message.text == 'لیست سکوت':
            	if self.silent_users:
            		mentions = ', '.join([utils.Mention("کاربر", x)
            		for x in self.silent_users])
            		await update.reply(mentions)
            	else:
            		await update.reply('لیست سکوت خالی است.')


    async def check_silent_users(self, update: Updates):
        if update.message.author_object_guid in self.silent_users:
            await self.delete_messages(update.object_guid, update.message.message_id)

bot = Bot('sokot')
bot.on_message_updates()(bot.handle_updates)
bot.on_message_updates()(bot.check_silent_users)
bot.run()
