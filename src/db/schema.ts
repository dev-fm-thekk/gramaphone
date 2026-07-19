import { pgTable, uuid, varchar, text, foreignKey, primaryKey, unique } from "drizzle-orm/pg-core"
import { sql } from "drizzle-orm"



export const applicant = pgTable("applicant", {
	id: uuid().defaultRandom().primaryKey(),
	name: varchar({ length: 100 }).notNull(),
	email: varchar({ length: 50 }).notNull(),
	phone: varchar({ length: 10 }).notNull(),
}, (table) => [
	unique("applicant_email_key").on(table.email),	unique("applicant_phone_key").on(table.phone),]);

export const application = pgTable("application", {
	id: uuid().defaultRandom().primaryKey(),
	applicantId: uuid("applicant_id").notNull().references(() => applicant.id),
	poc: uuid().notNull().references(() => users.id),
	doc: text().notNull(),
	updates: text(),
	status: text(),
});

export const users = pgTable("users", {
	id: uuid().defaultRandom().primaryKey(),
	name: varchar({ length: 100 }).notNull(),
	email: varchar({ length: 50 }).notNull(),
	role: text(),
	password: varchar({ length: 50 }),
	refreshToken: varchar("refresh_token", { length: 100 }),
}, (table) => [
	unique("users_email_key").on(table.email),]);
