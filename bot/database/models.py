from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from vkbottle_types.responses.utils import UtilsShortLink


class PromocodeModel(BaseModel):
    key: str
    apples_type: str
    reward: int
    limit: int
    used_by: List[int] = Field(default=[])


class Apples(BaseModel):
    green: int = Field(default=0)
    red: int = Field(default=0)


class DailyBonus(BaseModel):
    time: Optional[datetime] = Field(default=None)

    @property
    def is_available(self):
        if self.time is None:
            return True

        if self.time and int(datetime.utcnow().timestamp() - self.time.timestamp()) >= 86400:
            return True
        return False

    @property
    def time_left(self):
        return int((86400 - int(datetime.utcnow().timestamp() - self.time.timestamp())) / 60)

    def get(self):
        self.time = datetime.utcnow()


class CommentBouns(BaseModel):
    time: Optional[datetime] = Field(default=None)

    @property
    def is_available(self):
        if self.time is None:
            return True

        if int(datetime.utcnow().timestamp() - self.time.timestamp()) >= 5400:
            return True
        return False

    @property
    def time_left(self):
        return int((5400 - int(datetime.utcnow().timestamp() - self.time.timestamp())) / 60)

    def get(self):
        self.time = datetime.utcnow()


class Bonuses(BaseModel):
    daily: DailyBonus = DailyBonus()
    gaming: DailyBonus = DailyBonus()
    comment: CommentBouns = CommentBouns()


class Referrals(BaseModel):
    parent: Optional[int] = Field(default=None)
    my: List[int] = Field(default=list())
    link: Optional[UtilsShortLink] = Field(default=None)

    @property
    def count(self) -> int:
        return len(self.my)


class LikesQuest(BaseModel):
    posts: List[int] = Field(default=list())

    @property
    def is_complete(self):
        if len(self.posts) == 50:
            return True
        return False

    @property
    def count(self):
        return len(self.posts)


class ReferralsQuest(BaseModel):
    peoples: List[int] = Field(default=list())

    @property
    def is_complete(self):
        if len(self.peoples) == 10:
            return True
        return False

    @property
    def count(self):
        return len(self.peoples)


class MarketQuest(BaseModel):
    purchased: int = Field(default=0)

    @property
    def is_complete(self):
        if self.purchased == 3:
            return True
        return False


class Quests(BaseModel):
    likes: LikesQuest = LikesQuest()
    referrals: ReferralsQuest = ReferralsQuest()
    market: MarketQuest = MarketQuest()


class UserModel(BaseModel):
    id: int
    apples: Apples = Apples()
    bonuses: Bonuses = Bonuses()
    referrals: Referrals = Referrals()
    quests: Quests = Quests()
