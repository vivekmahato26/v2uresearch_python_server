from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from users.models import Region

class RegionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. Check for explicit Region Switch via Query Param
        set_region = request.GET.get('set_region')
        if set_region:
            request.region_to_set = set_region.upper()
            # CRITICAL FIX: Update request.COOKIES immediately so views/mixins see the NEW region
            # during this request cycle, avoiding the "double click" issue.
            request.COOKIES['region'] = request.region_to_set
            
            # If we are setting the region, we don't need to do login check immediately
            # as this request will set the cookie.
            return None

        # 2. Login Logic: Enforce User's Region
        if request.user.is_authenticated:
            try:
                # Access profile safely
                profile = getattr(request.user, 'userprofile', None)
                if profile and profile.region:
                    user_region_code = profile.region.country_code
                    current_cookie = request.COOKIES.get('region')
                    
                    # If cookie is different from user's region, force a switch
                    # This acts like a "header selector" triggered by login
                    if current_cookie != user_region_code:
                        # Prevent infinite redirect loops if we are already on the target domain/param
                        # But here, we just redirect appends set_region param
                        
                        # Logic for cross-domain redirect if needed
                        # Simplification: Just redirect to CURRENT URL with set_region param
                        # The switchCountry view handles domain switching.
                        # BUT, we are in middleware.
                        # If we just add ?set_region=CODE, the middleware (in next request) sets cookie.
                        # But if the domain is wrong, setting cookie on WRONG domain is useless.
                        
                        # We need to know if we are on the wrong domain.
                        # Check Region object for hostname.
                        target_region = profile.region
                        current_host = request.get_host()
                        
                        # If target region has a specific hostname and we are not on it:
                        # Redirect to that hostname
                        if target_region.region_hostname and target_region.region_hostname not in current_host:
                            # Build new URL
                            protocol = "https" if request.is_secure() else "http"
                            new_url = f"{protocol}://{target_region.region_hostname}{request.path}?set_region={user_region_code}"
                            return redirect(new_url)
                        
                        # Even if on same domain, we need to update the cookie
                        # So we redirect with ?set_region param to trigger step 1
                        query_string = request.GET.copy()
                        query_string['set_region'] = user_region_code
                        return redirect(f"{request.path}?{query_string.urlencode()}")

            except Exception as e:
                # Fail silently or log
                print(f"RegionMiddleware Error: {e}")
                pass
        
        return None

    def process_response(self, request, response):
        # If a region was requested to be set, set the cookie on the response
        if hasattr(request, 'region_to_set'):
            # Set for 1 year
            response.set_cookie('region', request.region_to_set, max_age=31536000)
        return response
