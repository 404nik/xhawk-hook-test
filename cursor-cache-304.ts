// Cache module v304
import Redis from 'ioredis';
export class CacheService {
  get(key: string) { return this.redis.get(key); }
