"""MCP Server - FastMCP Edition (Backend Only)"""

from fastmcp import FastMCP
from datetime import datetime
import pytz
from starlette.responses import Response
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware

mcp = FastMCP("demo-mcp-server")

# CORS Middleware to add headers to all responses
class CORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Handle OPTIONS preflight
        if request.method == "OPTIONS":
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Credentials": "true",
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add CORS headers to response
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response

# Add CORS middleware
mcp.add_middleware(CORSMiddleware)

# Store tool functions for direct HTTP access
TOOL_FUNCTIONS = {}

# Custom HTTP routes for direct tool access
async def call_tool_http(request):
    """Direct HTTP access to tools"""
    # Handle OPTIONS preflight request
    if request.method == "OPTIONS":
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
    
    import json
    import traceback
    tool_name = request.path_params['tool_name']
    body = await request.body()
    params = json.loads(body) if body else {}
    
    print(f"[DEBUG] Tool call: {tool_name}")
    print(f"[DEBUG] Parameters: {params}")
    print(f"[DEBUG] Available tools: {list(TOOL_FUNCTIONS.keys())}")
    
    try:
        # Get the tool function
        if tool_name not in TOOL_FUNCTIONS:
            return Response(
                status_code=404,
                content=f"Tool '{tool_name}' not found",
                media_type="text/plain",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                }
            )
        
        # Execute the tool
        print(f"[DEBUG] Executing tool: {tool_name}")
        result = TOOL_FUNCTIONS[tool_name](**params)
        print(f"[DEBUG] Result: {result}")
        return Response(
            status_code=200,
            content=result,
            media_type="text/plain",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        error_detail = traceback.format_exc()
        print(f"[ERROR] {error_detail}")
        return Response(
            status_code=500,
            content=f"Error: {str(e)}\n{error_detail}",
            media_type="text/plain",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )

# Add custom routes
mcp._additional_http_routes = [
    Route("/tools/{tool_name}", call_tool_http, methods=["POST", "OPTIONS"]),
]

def get_weather(city: str) -> str:
    """Get weather information for a city."""
    weather_data = {
        "temperature": 22,
        "condition": "Sunny",
        "humidity": 65,
        "wind_speed": 10
    }
    result = f"Weather in {city}:\n"
    result += f"Temperature: {weather_data['temperature']}°C\n"
    result += f"Condition: {weather_data['condition']}\n"
    result += f"Humidity: {weather_data['humidity']}%\n"
    result += f"Wind Speed: {weather_data['wind_speed']} km/h"
    return result

TOOL_FUNCTIONS['get_weather'] = get_weather
mcp.tool()(get_weather)

def calculate(operation: str, a: float, b: float) -> str:
    """Perform basic arithmetic calculations."""
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return f"Unknown operation: {operation}"
    return f"{a} {operation} {b} = {result}"

TOOL_FUNCTIONS['calculate'] = calculate
mcp.tool()(calculate)

def get_time(timezone: str = "UTC") -> str:
    """Get current time in a specific timezone."""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Unknown timezone: {timezone}"

TOOL_FUNCTIONS['get_time'] = get_time
mcp.tool()(get_time)

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency between different units (simulated rates)."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "GBP": 0.73,
        "JPY": 110.0,
        "CAD": 1.25,
        "AUD": 1.35
    }
    
    if from_currency not in rates or to_currency not in rates:
        return f"Unsupported currency. Available: {', '.join(rates.keys())}"
    
    usd_amount = amount / rates[from_currency]
    converted = usd_amount * rates[to_currency]
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"

TOOL_FUNCTIONS['convert_currency'] = convert_currency
mcp.tool()(convert_currency)

@mcp.resource("resource://messages")
def get_messages() -> str:
    """Server Messages - Collection of server messages and logs."""
    return "Welcome to the MCP Server!\nThis is a demo resource containing server information."

@mcp.prompt()
def greeting() -> str:
    """A friendly greeting prompt."""
    return "Hello! I'm an MCP server. How can I help you today?"

@mcp.prompt()
def help() -> str:
    """Get help with using the server."""
    return """Available tools:
- get_weather: Get weather for a city
- calculate: Perform calculations
- get_time: Get current time
- convert_currency: Convert currencies"""

if __name__ == "__main__":
    # Run FastMCP server with SSE transport on port 8001 (shows official FastMCP branding)
    # Bind to 0.0.0.0 to allow access from external browsers
    mcp.run(transport="sse", host="0.0.0.0", port=8001)