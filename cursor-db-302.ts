// Database module v302
export class Database { pool: any; }
  connect(url: string) { this.pool = createPool(url); }
