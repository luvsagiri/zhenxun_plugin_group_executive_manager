from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg, Command
from basic_plugins.ban import parse_ban_time
from configs.config import NICKNAME
from models.level_user import LevelUser
from utils.utils import get_message_at, is_number
from typing import Tuple, Union

__zx_plugin_name__ = "群管理"
__plugin_type__ = ("一些工具",)
__plugin_usage__ = """
usage：
    简易群管
    PS：
    艾特全体是没有用的，不要打扰别人啦
    ------------------------
    群主、超级管理员 可用：
    设置管理权限+@
    取消管理权限+@
    ------------------------
    群主、群管理 可用
    禁言+@+小时数
    踢+@
    PS：
    解禁用 禁言+@+0
"""
__plugin_des__ = "群管助手/设置执行管理员"
__plugin_cmd__ = ["设置执行管理", "取消执行管理", "踢", "禁言", ]
__plugin_version__ = 0.1
__plugin_author__ = "luvsagiri"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__,
}
ban = on_command("禁言", block=True, priority=5)  # 小时
kick = on_command("踢", aliases={"移出本群"}, block=True, priority=5)
executive_manager = on_command(
    "设置管理权限",
    aliases={"取消管理权限", "添加管理权限", "删除管理权限"},
    priority=5,
    block=True,
)


@executive_manager.handle()
async def _(bot: Bot, event: GroupMessageEvent, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg(), ):
    result = ""
    user_info = await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id)
    if user_info["role"] != "owner" and str(event.user_id) not in list(bot.config.superusers):
        await executive_manager.finish(f"只有群主才能管理权限，爪巴！")
    qqs = get_message_at(event.json())
    if cmd[0][:2] in ["添加", "设置"]:
        for qq in qqs:
            if await LevelUser.set_level(qq, event.group_id, 5, 1):
                result = f"添加管理成功, 权限: 5"
            else:
                result = f"管理已存在, 更新权限: 5"
    else:
        for qq in qqs:
            if await LevelUser.delete_level(qq, event.group_id):
                result = "删除管理成功!"
            else:
                result = "该账号无管理权限!"
    await executive_manager.finish(result)


@ban.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    time = parse_ban_time(msg)
    self_info = await bot.get_group_member_info(user_id=int(bot.self_id), group_id=event.group_id)
    if self_info["role"] not in ["admin", "owner"]:
        await ban.finish(f"{NICKNAME}还不是管理员呢,呜呜呜")
    if not time >= 0:
        await ban.finish("请携带禁言时长(小时数)")
    qqs = get_message_at(event.json())
    for qq in qqs:
        if LevelUser.get_user_level(qq, event.group_id) and LevelUser.get_user_level(qq, event.group_id) >= 5:
            await ban.send(f"对方是管理员,{NICKNAME}无权操作")
        await bot.set_group_ban(user_id=qq, group_id=event.group_id, duration=time)


@kick.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_info = await bot.get_group_member_info(user_id=int(bot.self_id), group_id=event.group_id)
    if user_info["role"] != "admin":
        await kick.finish(f"{NICKNAME}还不是管理员呢,呜呜呜")
    qqs = get_message_at(event.json())
    for qq in qqs:
        if LevelUser.get_user_level(qq, event.group_id) and LevelUser.get_user_level(qq, event.group_id) >= 5:
            await ban.send(f"对方是管理员,{NICKNAME}无权操作")
        await bot.set_group_kick(user_id=qq, group_id=event.group_id, reject_add_request=False)


def parse_ban_time(msg: str) -> Union[int, str]:
    """
    解析ban时长
    :param msg: 文本消息
    """
    if not msg:
        return -1
    msg = msg.split()
    if len(msg) == 1:
        if not is_number(msg[0].strip()):
            return "参数必须是数字！"
        return int(msg[0]) * 60 * 60
    else:
        if not is_number(msg[0].strip()) or not is_number(msg[1].strip()):
            return "参数必须是数字！"
        return int(msg[0]) * 60 * 60 + int(msg[1]) * 60
