//this is a rate limiter mdule for xhawk agent
export class RateLimiter {
  private tokens: number;
  private lastRefill: number;
  private readonly refillRate: number; // tokens per second
  private readonly capacity: number;
  
  constructor(refillRate: number, capacity: number) {   
    this.refillRate = refillRate;
    this.capacity = capacity;
    this.tokens = capacity; // start full
    this.lastRefill = Date.now();
  }

  private refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000; // convert ms to seconds
    const tokensToAdd = Math.floor(elapsed * this.refillRate);
    
    if (tokensToAdd > 0) {
      this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
      this.lastRefill = now;
    }   
    }

    public tryRemoveTokens(count: number): boolean {
        this.refill();
        if (this.tokens >= count) {
            this.tokens -= count;
            return true;
        }
        return false;
    }
}