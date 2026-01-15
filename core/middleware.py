from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Basic security headers
        response.setdefault('X-Frame-Options', 'DENY')
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('Referrer-Policy', 'no-referrer-when-downgrade')
        response.setdefault('Permissions-Policy', "geolocation=(), microphone=()")
        # Content Security Policy - adjust as needed
        response.setdefault('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:;")
        return response
