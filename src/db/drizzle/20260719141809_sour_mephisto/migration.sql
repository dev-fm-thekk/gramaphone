-- Current sql file was generated after introspecting the database
-- If you want to run this migration please uncomment this code before executing migrations
/*
CREATE TABLE "applicant" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"name" varchar(100) NOT NULL,
	"email" varchar(50) NOT NULL CONSTRAINT "applicant_email_key" UNIQUE,
	"phone" varchar(10) NOT NULL CONSTRAINT "applicant_phone_key" UNIQUE
);
--> statement-breakpoint
CREATE TABLE "application" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"applicant_id" uuid NOT NULL,
	"poc" uuid NOT NULL,
	"doc" text NOT NULL,
	"updates" text,
	"status" text
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	"name" varchar(100) NOT NULL,
	"email" varchar(50) NOT NULL CONSTRAINT "users_email_key" UNIQUE,
	"role" text,
	"password" varchar(50),
	"refresh_token" varchar(100)
);
--> statement-breakpoint
ALTER TABLE "application" ADD CONSTRAINT "application_applicant_id_fkey" FOREIGN KEY ("applicant_id") REFERENCES "applicant"("id");--> statement-breakpoint
ALTER TABLE "application" ADD CONSTRAINT "application_poc_fkey" FOREIGN KEY ("poc") REFERENCES "users"("id");
*/