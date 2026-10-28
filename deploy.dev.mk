


# Set ENV_FILE variable if it wasn't set already (for example, through shell)
ENV_FILE ?= ./deploy-dev/test-chat.tg-bot-python.dev.env
TG_ENV_FILE ?= ./deploy-dev/test-chat.tg-bot-python.dev.tg.env

# Load env vars from file to shell
ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    export
endif

ifneq (,$(wildcard $(TG_ENV_FILE)))
    include $(TG_ENV_FILE)
    export
endif



dev:
	uv run bot.py
