#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, utils, enums
from pyrogram import types


class SendMessage:
    async def send_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None,
        message_thread_id: int = None,
        text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        schedule_date: datetime = None
    ) -> "types.Message":
        """Send text messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            text (``str``):
                Text of the message to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent text message is returned.

        Example:
            .. code-block:: python

                # Simple example
                await app.send_message(chat_id="me", text="Message sent with **Pyrogram**!")

                # Disable web page previews
                await app.send_message(
                    chat_id="me", text="https://docs.pyrogram.org",
                    link_preview_options=types.LinkPreviewOption(
                        is_disabled=True
                    )
                )

                # Reply to a message using its id
                await app.send_message(chat_id="me", text="this is a reply", reply_parameters=types.ReplyParameters(message_id=123))

            .. code-block:: python

                # For bots only, send messages with keyboards attached

                from pyrogram.types import (
                    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)

                # Send a normal keyboard
                await app.send_message(
                    chat_id=chat_id, text="Look at that button!",
                    reply_markup=ReplyKeyboardMarkup([["Nice!"]]))

                # Send an inline keyboard
                await app.send_message(
                    chat_id=chat_id, text="These are inline buttons",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Data", callback_data="callback_data")],
                            [InlineKeyboardButton("Docs", url="https://docs.pyrogram.org")]
                        ]))
        """

        reply_to = await utils.get_reply_head_fm(
            self,
            message_thread_id,
            reply_parameters
        )
        message, entities = (await utils.parse_text_entities(self, text, parse_mode, entities)).values()

        if (
            link_preview_options and
            link_preview_options.url
        ):
            r = await self.invoke(
                raw.functions.messages.SendMedia(
                    peer=await self.resolve_peer(chat_id),
                    silent=disable_notification or None,
                    reply_to=reply_to,
                    random_id=self.rnd_id(),
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    reply_markup=await reply_markup.write(self) if reply_markup else None,
                    message=message,
                    media=raw.types.InputMediaWebPage(
                        url=link_preview_options.url,
                        force_large_media=link_preview_options.prefer_large_media,
                        force_small_media=link_preview_options.prefer_small_media
                    ),
                    invert_media=link_preview_options.show_above_text,
                    entities=entities,
                    noforwards=protect_content
                )
            )

        elif message:
            r = await self.invoke(
                raw.functions.messages.SendMessage(
                    peer=await self.resolve_peer(chat_id),
                    no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                    silent=disable_notification or None,
                    # TODO
                    # TODO
                    noforwards=protect_content,
                    # TODO
                    invert_media=link_preview_options.show_above_text if link_preview_options else None,
                    reply_to=reply_to,
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    reply_markup=await reply_markup.write(self) if reply_markup else None,
                    # TODO
                    random_id=self.rnd_id(),
                    message=message,
                    entities=entities,
                )
            )

        else:
            # TODO
            return types.Message(
                id=0,
                # TODO
                date=utils.timestamp_to_datetime(0),
            )

        if isinstance(r, raw.types.UpdateShortSentMessage):
            peer = await self.resolve_peer(chat_id)

            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                id=r.id,
                chat=types.Chat(
                    id=peer_id,
                    type=enums.ChatType.PRIVATE,
                    client=self
                ),
                text=message,
                date=utils.timestamp_to_datetime(r.date),
                outgoing=r.out,
                reply_markup=reply_markup,
                entities=[
                    types.MessageEntity._parse(None, entity, {})
                    for entity in entities
                ] if entities else None,
                client=self
            )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage)
                )
