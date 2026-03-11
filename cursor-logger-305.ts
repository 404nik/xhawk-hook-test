// Logger module v305
type Level = 'debug'|'info'|'warn'|'error';
export class Logger {
  constructor(private level: Level = 'info') {}
