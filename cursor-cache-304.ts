// Cache module v304
import Redis from 'ioredis';
export class CacheService {
  get(key: string) { return this.redis.get(key); }
  set(key: string, val: string, ttl?: number) {}
  del(key: string) { return this.redis.del(key); }
  flush() { return this.redis.flushdb(); }
