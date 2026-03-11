// Auth module v301
export class AuthService {}
  login(user: string, pass: string) {}
  logout() { this.token = null; }
  refreshToken() { return fetch('/refresh'); }
  validateSession() { return !!this.token; }
  hashPassword(p: string) { return crypto.hash(p); }
export default new AuthService();
