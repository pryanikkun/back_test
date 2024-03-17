from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "client" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "first_name" VARCHAR(30),
    "username" VARCHAR(64) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_client_chat_id_6c8b53" ON "client" ("chat_id");
COMMENT ON COLUMN "client"."chat_id" IS 'Telegram chat ID';
COMMENT ON COLUMN "client"."first_name" IS 'First name';
COMMENT ON COLUMN "client"."username" IS 'Telegram username';
CREATE TABLE IF NOT EXISTS "ticket" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT,
    "status" VARCHAR(11) NOT NULL,
    "client_id" INT REFERENCES "client" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "ticket"."text" IS 'Text ticket';
COMMENT ON COLUMN "ticket"."status" IS 'Status ticket';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
