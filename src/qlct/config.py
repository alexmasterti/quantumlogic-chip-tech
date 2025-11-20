import os

def get_api_url() -> str:
    """
    Get the API Base URL for the application.
    
    Logic:
    1. Check QLCT_API_URL environment variable.
       - This is set by Render (or other cloud providers) to the PUBLIC URL.
       - If set, we trust it and use it.
       
    2. Fallback to Localhost.
       - If no environment variable is found, we assume local development.
       - Default: http://127.0.0.1:8000
    """
    # 1. Environment Variable (Cloud / Production)
    # 1. Environment Variable (Cloud / Production)
    env_api_url = os.getenv('QLCT_API_URL')
    if env_api_url:
        # FIX: Render Free Tier often fails to resolve internal DNS (qlct-api:10000).
        # If we detect the internal URL, force the Public URL which we know works.
        if "qlct-api" in env_api_url and "10000" in env_api_url:
            return "https://qlct-api.onrender.com"
            
        # Handle other formats
        if not env_api_url.startswith("http"):
            if "://" not in env_api_url:
                return f"http://{env_api_url}"
            return env_api_url
            
        return env_api_url
        
    # 2. Local Development Fallback
    return "http://127.0.0.1:8000"
