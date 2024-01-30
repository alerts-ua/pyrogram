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

from pyrogram import raw
from ..object import Object


class ChatPermissions(Object):
    """Describes actions that a non-administrator user is allowed to take in a chat.

    Parameters:
        can_send_messages (``bool``, *optional*):
            True, if the user is allowed to send text messages, contacts, giveaways, giveaway winners, invoices, locations and venues

        can_send_audios (``bool``, *optional*):
            True, if the user is allowed to send audios

        can_send_documents
            True, if the user is allowed to send documents

        can_send_photos
            True, if the user is allowed to send photos

        can_send_videos
            True, if the user is allowed to send videos

        can_send_video_notes
            True, if the user is allowed to send video notes

        can_send_voice_notes
            True, if the user is allowed to send voice notes

        can_send_polls (``bool``, *optional*):
            True, if the user is allowed to send polls

        can_send_other_messages (``bool``, *optional*):
            True, if the user is allowed to send animations, games, stickers and use inline bots

        can_add_web_page_previews (``bool``, *optional*):
            True, if the user is allowed to add web page previews to their messages

        can_change_info (``bool``, *optional*):
            True, if the user is allowed to change the chat title, photo and other settings
            Ignored in public supergroups

        can_invite_users (``bool``, *optional*):
            True, if the user is allowed to invite new users to the chat

        can_pin_messages (``bool``, *optional*):
            True, if the user is allowed to pin messages
            Ignored in public supergroups

        can_manage_topics (``bool``, *optional*):
            True, if the user is allowed to create forum topics
            If omitted defaults to the value of can_pin_messages

        can_send_media_messages (``bool``, *optional*):
            True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes.
            Implies *can_send_messages*.
    """

    def __init__(
        self,
        *,
        can_send_messages: bool = None,  # Text, contacts, giveaways, giveaway winners, invoices, locations and venues
        can_send_audios: bool = None,
        can_send_documents: bool = None,
        can_send_photos: bool = None,
        can_send_videos: bool = None,
        can_send_video_notes: bool = None,
        can_send_voice_notes: bool = None,
        can_send_polls: bool = None,
        can_send_other_messages: bool = None,  # animations, games, stickers, inline bots
        can_add_web_page_previews: bool = None,
        can_change_info: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None,
        can_manage_topics: bool = None,
        can_send_media_messages: bool = None,  # Audio files, documents, photos, videos, video notes and voice notes
    ):
        super().__init__(None)

        self.can_send_messages = can_send_messages
        self.can_send_audios = can_send_audios
        self.can_send_documents = can_send_documents
        self.can_send_photos = can_send_photos
        self.can_send_videos = can_send_videos
        self.can_send_video_notes = can_send_video_notes
        self.can_send_voice_notes = can_send_voice_notes
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.can_manage_topics = can_manage_topics
        self.can_send_media_messages = can_send_media_messages

    @staticmethod
    def _parse(denied_permissions: "raw.base.ChatBannedRights") -> "ChatPermissions":
        if isinstance(denied_permissions, raw.types.ChatBannedRights):
            return ChatPermissions(
                can_send_messages=not denied_permissions.send_messages,
                can_send_audios=not denied_permissions.send_audios,
                can_send_documents=not denied_permissions.send_docs,
                can_send_photos=not denied_permissions.send_photos,
                can_send_videos=not denied_permissions.send_videos,
                can_send_video_notes=not denied_permissions.send_roundvideos,
                can_send_voice_notes=not denied_permissions.send_voices,
                can_send_polls=not denied_permissions.send_polls,
                can_send_media_messages=not denied_permissions.send_media,
                can_send_other_messages=any([
                    not denied_permissions.send_stickers,
                    not denied_permissions.send_gifs,
                    not denied_permissions.send_games,
                    not denied_permissions.send_inline
                ]),
                can_add_web_page_previews=not denied_permissions.embed_links,
                can_change_info=not denied_permissions.change_info,
                can_invite_users=not denied_permissions.invite_users,
                can_pin_messages=not denied_permissions.pin_messages,
                can_manage_topics=not denied_permissions.manage_topics,
                can_send_media_messages=any([
                    not denied_permissions.send_audios,
                    not denied_permissions.send_docs,
                    not denied_permissions.send_photos,
                    not denied_permissions.send_videos,
                    not denied_permissions.send_roundvideos,
                    not denied_permissions.send_voices
                ])
            )
