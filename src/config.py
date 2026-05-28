"""配置管理模块"""
from datetime import date
from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """fxsa-commit 配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="FXSA_",
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
    hour: int = Field(default=12, ge=0, le=23, description="提交小时 (0-23)")

    # 内置常量
    COMMIT_TEMPLATE: ClassVar[str] = "Update on {date}"
    REPO_PATH: ClassVar[Path] = Path(".")

    def validate_dates(self) -> None:
        """验证日期范围"""
        if self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date")

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
