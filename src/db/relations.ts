import { defineRelations } from "drizzle-orm";
import * as schema from "./schema";

export const relations = defineRelations(schema, (r) => ({
	applicant: {
		users: r.many.users({
			from: r.applicant.id.through(r.application.applicantId),
			to: r.users.id.through(r.application.poc)
		}),
	},
	users: {
		applicants: r.many.applicant(),
	},
}))