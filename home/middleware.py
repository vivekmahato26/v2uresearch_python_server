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

        # 2. Login Logic: Enforce User's Region (ONCE PER SESSION)
        # We use a session flag to ensure we don't override manual switches later.
        if request.user.is_authenticated and not request.session.get('region_checked', False):
            request.session['region_checked'] = True
            try:
                # Access profile safely
                profile = getattr(request.user, 'userprofile', None)
                if profile and profile.region:
                    user_region_code = profile.region.country_code
                    current_cookie = request.COOKIES.get('region')
                    
                    # If cookie is different from user's region, force a switch
                    if current_cookie != user_region_code:
                         # Redirect Logic...
                        target_region = profile.region
                        current_host = request.get_host()
                        
                        if target_region.region_hostname and target_region.region_hostname not in current_host:
                            protocol = "https" if request.is_secure() else "http"
                            new_url = f"{protocol}://{target_region.region_hostname}{request.path}?set_region={user_region_code}"
                            return redirect(new_url)
                        
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
