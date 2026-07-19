import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';
import vars from '../config';

export default defineConfig({
  out: './drizzle',
  schema: './db/schema.ts',
  dialect: 'postgresql',
  dbCredentials: {
    url: vars.DATABASE_URL!,
  },
});
