from services.db_context import db


class Executive_managers(db.Model):
    __tablename__ = "executive_managers"
    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)

    _idx1 = db.Index("executive_managers_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def is_executive_managers(cls, user_qq: int, group_id: int) -> bool:
        """
        说明:
            查询是否是执行管理
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.gino.first()
        if not user:
            return False
        else:
            return True

    @classmethod
    async def unset_executive_managers(cls, user_qq: int, group_id: int) -> bool:
        """
        说明:
            移除执行管理
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        try:
            await cls.delete.where(
                (cls.user_qq == user_qq)
                & (cls.group_id == group_id)
            ).gino.status()
        except:
            return False
        else:
            return True


    @classmethod
    async def set_executive_managers(cls, user_qq: int, group_id: int) -> bool:
        """
        说明:
            添加执行管理
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        try:
            await cls.create(user_qq=user_qq, group_id=group_id)
        except:
            return True
        else:
            return True
