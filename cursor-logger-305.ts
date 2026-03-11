// Logger module v305
type Level = 'debug'|'info'|'warn'|'error';
export class Logger {
  constructor(private level: Level = 'info') {}
  debug(msg: string) { if (this.level === 'debug') console.log(msg); }
  info(msg: string) { console.log('[INFO]', msg); }
