from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    SYSTEM_PROMPT: str = "Ты — Газпромбанк, русскоязычный генератор маркетинговых текстов и создания рекламы банка. Ты помогаешь продавать людям банковские услуги(кредиты, ипотеки, обслуживание). Ты предлаешь оформить карту 'Мир' и воспользоваться мобильным приложением банка."
    SYSTEM_TOKEN: int = 1587
    USER_TOKEN: int = 2188
    BOT_TOKEN: int = 12435
    LINEBREAK_TOKEN: int = 13
    PATH: str = "model-q4_K.gguf"
    ROLE_TOKENS: dict = {
        "user": USER_TOKEN,
        "bot": BOT_TOKEN,
        "system": SYSTEM_TOKEN
    }

    model_config = SettingsConfigDict(env_prefix='env.model')


model_settings = ModelSettings()
