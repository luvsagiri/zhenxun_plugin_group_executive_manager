from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg
from basic_plugins.ban import parse_ban_time
from configs.config import NICKNAME
from utils.utils import get_message_at
from .model import *

__zx_plugin_name__ = "群管理"
__plugin_type__ = ("一些工具",)
__plugin_usage__ = """
usage：
    设置超过数量限制的隐形群管理员
    简易群管
    PS：
    艾特全体是没有用的，不要打扰别人啦
    ------------------------
    群主、超级管理员 可用：
    设置执行管理+@
    取消执行管理+@
    ------------------------
    群主、群管理、执行管理 可用
    禁言+@+小时数
    踢+@
    PS：
    解禁用 禁言+@+0
"""
__plugin_des__ = "群管助手/设置执行管理员"
__plugin_cmd__ = ["设置执行管理"]
__plugin_version__ = 0.1
__plugin_author__ = "luvsagiri"

set_executive_manager = on_command("设置执行管理", block=True, priority=5)
unset_executive_manager = on_command("取消执行管理", block=True, priority=5)
ban = on_command("禁言", block=True, priority=5)  # 小时
kick = on_command("踢", aliases={"移出本群"}, block=True, priority=5)


@set_executive_manager.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_info = await bot.get_group_member_info(user_id=int(bot.self_id), group_id=event.group_id)
    if user_info["role"] != "admin":
        await set_executive_manager.finish(f"{NICKNAME}还不是管理员呢，告辞！")
    user_info = await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id)
    if user_info["role"] != "owner" and str(event.user_id) not in list(bot.config.superusers):
        await set_executive_manager.finish(f"只有群主才能设置执行管理，告辞！")
    qqs = get_message_at(event.json())
    for qq in qqs:
        if await Executive_managers.set_executive_managers(qq, event.group_id):
            await set_executive_manager.send(f"成功添加{qq}为本群执行管理!")
        else:
            await set_executive_manager.send(f"添加执行管理{qq}失败...")


@unset_executive_manager.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_info = await bot.get_group_member_info(user_id=int(bot.self_id), group_id=event.group_id)
    if user_info["role"] != "admin":
        await unset_executive_manager.finish(f"{NICKNAME}还不是管理员呢，告辞！")
    user_info = await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id)
    if user_info["role"] != "owner" and str(event.user_id) not in list(bot.config.superusers):
        await unset_executive_manager.finish(f"只有群主才能取消执行管理，告辞！")
    qqs = get_message_at(event.json())
    for qq in qqs:
        if await Executive_managers.unset_executive_managers(qq, event.group_id):
            await unset_executive_manager.send(f"成功取消{qq}的执行管理!")
        else:
            await unset_executive_manager.send(f"取消执行管理{qq}失败...")


@ban.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    time = parse_ban_time(msg)
    if not time >= 0:
        await ban.finish("请输入禁言时长")
    user_info = await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id, no_cache=True)
    if user_info["role"] not in ["owner", "admin"]:
        if not await Executive_managers.is_executive_managers(event.user_id, event.group_id):
            await ban.finish("你还不是管理员哦，想什么呢？")
    user_info = await bot.get_group_member_info(user_id=int(bot.self_id), group_id=event.group_id)
    if user_info["role"] != "admin":
        await ban.finish(f"{NICKNAME}还不是管理员呢，告辞！")
    qqs = get_message_at(event.json())
    for qq in qqs:
        await bot.set_group_ban(user_id=qq, group_id=event.group_id, duration=time)


@kick.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_info = await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id, no_cache=True)
    if user_info["role"] not in ["owner", "admin"]:
        if not await Executive_managers.is_executive_managers(event.user_id, event.group_id):
            await kick.finish("你还不是管理员哦，想什么呢？")
    user_info = await bot.get_group_member_info(user_id=int(bot.self_id), group_id=event.group_id)
    if user_info["role"] != "admin":
        await kick.finish(f"{NICKNAME}还不是管理员呢，告辞！")
    qqs = get_message_at(event.json())
    for qq in qqs:
        await bot.set_group_kick(user_id=qq, group_id=event.group_id, reject_add_request=False)
