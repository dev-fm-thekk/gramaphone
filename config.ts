import dotenv from 'dotenv';

dotenv.config();

const vars = {
    DATABASE_URL: process.env.DATABASE_URL
}

export default vars;