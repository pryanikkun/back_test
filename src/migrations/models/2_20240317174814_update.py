from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "message" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT,
    "ticket_id" INT REFERENCES "ticket" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "message"."text" IS 'Messsage ticket';;
        ALTER TABLE "ticket" DROP COLUMN "text";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "ticket" ADD "text" TEXT;
        DROP TABLE IF EXISTS "message";"""
