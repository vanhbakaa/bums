from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str


    REF_LINK: str = ""

    AUTO_TAP: bool = True
    MIN_ENERGY: int = 500
    RANDOM_TAP_TIMES: list[int] = [5, 10]
    SLEEP_BETWEEN_TAPS: list[int] = [20, 30]


    AUTO_TASK: bool = True
    BLACK_LIST_TASKS: list[str] = ["invite 1 friend", "Promote TON Blockchain", "Boost channel", "Boinkers: Spin the Slut 10 times"]

    AUTO_JOIN_GANG: bool = True
    GANG_TO_JOIN: str = "vanhbakaaa"

    AUTO_UPGRADE_TAP: bool = True
    TAP_MAX_LVL: int = 9
    AUTO_UPGRADE_ENERGY: bool = True
    ENERGY_MAX_LVL: int = 5
    AUTO_UPGRADE_RECOVERY: bool = True
    RECOVERY_MAX_LVL: int = 9
    AUTO_UPGRADE_CRIT_MULTI: bool = True
    CRIT_MULTI_MAX_LVL: int = 5
    AUTO_UPGRADE_JACKPOT_CHANCE: bool = True
    JACKPOT_CHANCE_MAX_LVL: int = 5


    AUTO_UPGRADE_CARDS: bool = True

    AUTO_PLAY_SPIN: bool = True

    DELAY_EACH_ACCOUNT: list[int] = [20, 30]
    SLEEP_TIME_EACH_ROUND: list[int] = [1, 2]

    ADVANCED_ANTI_DETECTION: bool = True

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()

