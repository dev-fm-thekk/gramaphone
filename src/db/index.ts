import { drizzle } from 'drizzle-orm/node-postgres';
import vars from '../../config';

const db = drizzle(vars.DATABASE_URL!);

export default db;
