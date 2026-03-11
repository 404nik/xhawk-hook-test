// Database module v302
export class Database { pool: any; }
  connect(url: string) { this.pool = createPool(url); }
  query(sql: string) { return this.pool.query(sql); }
  transaction(fn: Function) { return this.pool.tx(fn); }
  migrate() { return runMigrations(this.pool); }
