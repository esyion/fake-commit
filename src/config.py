"""配置管理模块"""
import random
from datetime import date
from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """fake-commit 配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="FAKE_",
        extra="ignore",
    )

    # 必需配置
    author_name: str = Field(..., min_length=1, description="Git 提交用户名")
    author_email: str = Field(..., min_length=1, description="Git 提交邮箱")

    # 可选配置
    start_date: date = Field(default=date(2026, 1, 1), description="开始日期")
    end_date: date = Field(default=date(2026, 1, 31), description="结束日期")
    commits_per_day: int = Field(default=1, ge=1, description="每天提交次数")
    branch: str = Field(default="main", description="分支名")

    # 随机模式配置
    random_mode: bool = Field(default=False, description="随机提交开关")
    random_range: str = Field(default="1,10", description="随机区间，格式 'min,max'")

    # 内置常量
    COMMIT_TEMPLATE: ClassVar[str] = "Update on {date}"
    REPO_PATH: ClassVar[Path] = Path(".")
    HOUR_RANGE: ClassVar[tuple[int, int]] = (0, 23)
    MINUTE_RANGE: ClassVar[tuple[int, int]] = (0, 59)
    SECOND_RANGE: ClassVar[tuple[int, int]] = (0, 59)

    def get_date_range(self) -> list[date]:
        """获取日期范围内的所有日期"""
        from datetime import timedelta
        dates = []
        current = self.start_date
        while current <= self.end_date:
            dates.append(current)
            current += timedelta(days=1)
        return dates

    def format_commit_message(self, commit_date: date) -> str:
        """格式化提交消息"""
        return self.COMMIT_TEMPLATE.format(date=commit_date.isoformat())

    def parse_random_range(self) -> tuple[int, int]:
        """解析随机区间"""
        parts = self.random_range.split(",")
        min_val = int(parts[0].strip())
        max_val = int(parts[1].strip())
        if min_val > max_val:
            raise ValueError("random_range min must be <= max")
        if min_val < 1:
            raise ValueError("random_range min must be >= 1")
        return (min_val, max_val)

    def get_commits_per_day(self) -> int:
        """获取每天提交次数"""
        if self.random_mode:
            min_val, max_val = self.parse_random_range()
            return random.randint(min_val, max_val)
        return self.commits_per_day