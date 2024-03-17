from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "employee" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(64) NOT NULL UNIQUE,
    "password" VARCHAR(64) NOT NULL,
    "first_name" VARCHAR(30),
    "last_name" VARCHAR(30)
);
CREATE INDEX IF NOT EXISTS "idx_employee_usernam_e8824b" ON "employee" ("username");
COMMENT ON COLUMN "employee"."username" IS 'Employee username';
COMMENT ON COLUMN "employee"."password" IS 'Password';
COMMENT ON COLUMN "employee"."first_name" IS 'First name';
COMMENT ON COLUMN "employee"."last_name" IS 'Last name';;
        ALTER TABLE "ticket" ADD "employee_id" INT;
        ALTER TABLE "ticket" ADD "ticket_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "ticket" ADD CONSTRAINT "fk_ticket_employee_f3d087df" FOREIGN KEY ("employee_id") REFERENCES "employee" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "ticket" DROP CONSTRAINT "fk_ticket_employee_f3d087df";
        ALTER TABLE "ticket" DROP COLUMN "employee_id";
        ALTER TABLE "ticket" DROP COLUMN "ticket_date";
        DROP TABLE IF EXISTS "employee";"""
