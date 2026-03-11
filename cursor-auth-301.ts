// Auth module v301
export class AuthService {}
  login(user: string, pass: string) {}
  logout() { this.token = null; }
  refreshToken() { return fetch('/refresh'); }
  validateSession() { return !!this.token; }
