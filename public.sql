-- ----------------------------
-- Table structure for apps
-- ----------------------------
DROP TABLE IF EXISTS "public"."apps";
CREATE TABLE "public"."apps" (
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "client_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "client_secret" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "tenant_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Primary Key structure for table apps
-- ----------------------------
ALTER TABLE "public"."apps" ADD CONSTRAINT "apps_pkey" PRIMARY KEY ("name");
