# MCP Client-Server Application

A complete Model Context Protocol (MCP) implementation with a FastMCP backend server and a web-based frontend client.

## 🏗️ Architecture

This project demonstrates a **separated client-server architecture**:

- **Backend (MCP Server)**: FastMCP server on port `8001` providing MCP protocol + REST API
- **Frontend (Client)**: Static web server on port `8000` serving the HTML/CSS/JavaScript interface

```
┌─────────────────────┐         ┌─────────────────────┐
│   Frontend Client   │         │   Backend Server    │
│   localhost:8000    │────────▶│   localhost:8001    │
│                     │  HTTP   │                     │
│  - HTML/CSS/JS      │  Fetch  │  - FastMCP 2.14.4   │
│  - User Interface   │ Requests│  - Tool Execution   │
│  - serve_client.py  │         │  - MCP Protocol     │
└─────────────────────┘         └─────────────────────┘
```

## 📁 Project Structure

```
MCPclient-server/
├── mcp-server/
│   ├── mcp_server.py          # FastMCP backend server
│   └── requirements.txt       # Python dependencies
│
├── mcp-client/
│   ├── index.html            # Frontend web interface
│   └── serve_client.py       # Static file server
│
└── README.md                 # This file
```

## 🚀 Features

### Backend (MCP Server)
- **Official FastMCP Implementation**: Uses FastMCP 2.14.4 with SSE transport
- **MCP Protocol Support**: Full MCP protocol at `/sse` endpoint
- **REST API**: Direct HTTP access to tools via `/tools/{tool_name}`
- **CORS Enabled**: Full cross-origin support for browser clients
- **4 Built-in Tools**:
  - Weather information
  - Mathematical calculator
  - Timezone converter
  - Currency converter

### Frontend (Client)
- **Modern Web UI**: Clean, responsive interface with gradient design
- **Real-time Tool Execution**: Direct fetch-based API calls
- **Status Monitoring**: Live server connection status
- **No Dependencies**: Pure HTML/CSS/JavaScript (no build process)

## 🛠️ Available Tools

| Tool | Description | Parameters | Example |
|------|-------------|------------|---------|
| `get_weather` | Get weather information for a city | `city: string` | London, Paris, Tokyo |
| `calculate` | Perform basic arithmetic | `operation: string, a: float, b: float` | add, subtract, multiply, divide |
| `get_time` | Get current time in timezone | `timezone: string` (optional, default: UTC) | UTC, America/New_York, Asia/Tokyo |
| `convert_currency` | Convert between currencies | `amount: float, from_currency: string, to_currency: string` | USD, EUR, GBP, JPY, CAD, AUD |

## 📋 Prerequisites

- **Python 3.8+** (tested with Python 3.13)
- **Conda environment** (recommended) or virtualenv
- **Modern web browser** (Chrome, Edge, Firefox)

## 🔧 Installation

### 1. Clone or navigate to the project directory
```bash
cd C:\Users\ZWJ1KOR\Desktop\code\Lecs\Projects\MCPclient-server
```

### 2. Create and activate conda environment
```bash
conda create -n testing python=3.13
conda activate testing
```

### 3. Install backend dependencies
```bash
cd mcp-server
pip install -r requirements.txt
```

**Dependencies:**
- `fastmcp>=2.14.0` - FastMCP framework
- `pytz==2024.1` - Timezone support
- `starlette` - ASGI framework (installed with FastMCP)
- `uvicorn` - ASGI server (installed with FastMCP)

## ▶️ Running the Application

### Start Both Servers

**Terminal 1 - Backend Server:**
```bash
conda activate testing
cd mcp-server
python mcp_server.py
```

**Terminal 2 - Frontend Server:**
```bash
conda activate testing
cd mcp-client
python serve_client.py
```

### Expected Output

**Backend (Port 8001):**
```
╭──────────────────────────────────────────────────────────╮
│                  ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█           │
│                  █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀           │
│                                                          │
│                     FastMCP 2.14.4                       │
│                  🖥  Server: demo-mcp-server              │
│                  📦 Transport: SSE                        │
│                  🔗 Server URL: http://0.0.0.0:8001/sse  │
╰──────────────────────────────────────────────────────────╯
```

**Frontend (Port 8000):**
```
============================================================
  Frontend Server Running
  URL: http://localhost:8000
  Directory: C:\...\mcp-client
============================================================
```

## 🌐 Accessing the Application

1. Open your web browser
2. Navigate to: **http://localhost:8000**
3. The interface should load with "Server: Online ✓" status
4. Click any tool button to test functionality

**⚠️ Important:** Always access via `http://localhost:8000`, NOT by opening `index.html` directly (file://), as this will cause CORS errors.

## 🔌 API Endpoints

### Backend Server (Port 8001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sse` | GET | MCP protocol SSE endpoint |
| `/tools/{tool_name}` | POST | Execute a specific tool |
| `/tools/{tool_name}` | OPTIONS | CORS preflight check |

### Example API Call

```javascript
// POST to http://localhost:8001/tools/get_weather
{
  "city": "London"
}

// Response (200 OK)
Weather in London:
Temperature: 22°C
Condition: Sunny
Humidity: 65%
Wind Speed: 10 km/h
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
taskkill /F /IM python.exe

# Then restart servers
```

### CORS Errors
- Ensure you're accessing `http://localhost:8000` (not `file://`)
- Check that both servers are running
- Verify backend shows "200 OK" for OPTIONS requests

### "Server: Offline" Status
- Verify backend is running on port 8001
- Check terminal for error messages
- Try hard refresh: `Ctrl + Shift + R`

### Cached Old Version
- Hard refresh: `Ctrl + Shift + R`
- Or open Incognito/Private window: `Ctrl + Shift + N`
- Clear browser cache

### No Data Displayed
- Open Developer Tools (F12)
- Check Console tab for errors
- Verify network requests show 200 OK responses
- Check that console.log shows received data

## 🔍 Debugging

### Enable Debug Logging
The backend already includes debug logging. Check terminal output for:
```
[DEBUG] Tool call: get_weather
[DEBUG] Parameters: {'city': 'London'}
[DEBUG] Available tools: ['get_weather', 'calculate', 'get_time', 'convert_currency']
[DEBUG] Executing tool: get_weather
[DEBUG] Result: Weather in London: ...
```

### Browser Console Logging
Frontend includes console.log statements. Open Developer Tools (F12) to see:
```
Getting weather for: London
Weather result: Weather in London: Temperature: 22°C...
```

## 📝 Code Overview

### Backend Server (`mcp-server/mcp_server.py`)

**Key Components:**
- `FastMCP("demo-mcp-server")` - Server initialization
- `CORSMiddleware` - Handles cross-origin requests
- `TOOL_FUNCTIONS = {}` - Direct function registry for HTTP access
- `call_tool_http()` - HTTP route handler for tool execution
- `@mcp.tool()` decorator - Registers tools with MCP protocol

**Tool Registration Pattern:**
```python
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    # Implementation
    return result

TOOL_FUNCTIONS['get_weather'] = get_weather  # For HTTP access
mcp.tool()(get_weather)  # For MCP protocol
```

### Frontend Client (`mcp-client/index.html`)

**Key Functions:**
- `callTool(toolName, params)` - Generic fetch wrapper for API calls
- `getWeather()`, `calculate()`, etc. - Tool-specific handlers
- Server status check on page load

**Configuration:**
```javascript
const BASE_URL = 'http://localhost:8001';  // Backend server URL
```

## 🔐 Security Notes

- **Development Only**: This setup is for development/demo purposes
- **No Authentication**: Tools are publicly accessible
- **CORS Wide Open**: `Access-Control-Allow-Origin: *` allows all origins
- **Input Validation**: Minimal validation on tool inputs

## 📚 MCP Protocol

The server implements the full MCP (Model Context Protocol) at:
- **SSE Endpoint**: `http://localhost:8001/sse`
- **Transport**: Server-Sent Events (SSE)
- **Features**: Tools, Resources, Prompts

While the web client uses direct HTTP calls for simplicity, the MCP protocol endpoint is available for MCP-compatible clients.

## 🎯 Future Enhancements

- [ ] Add authentication/authorization
- [ ] Implement real weather API integration
- [ ] Add more tools (file operations, database queries, etc.)
- [ ] WebSocket support for real-time updates
- [ ] Docker containerization
- [ ] Production deployment guide

## 📄 License

This is a demonstration project for educational purposes.

## 👥 Contributing

This is a learning/demo project. Feel free to fork and modify for your needs.

## 🆘 Support

If you encounter issues:
1. Check the Troubleshooting section
2. Verify both servers are running
3. Check browser Developer Console (F12)
4. Review server terminal logs

## 📞 Contact

For questions about MCP protocol: https://modelcontextprotocol.io
For FastMCP documentation: https://gofastmcp.com

---

**Built with:**
- [FastMCP](https://gofastmcp.com) - Official FastMCP framework
- [Starlette](https://www.starlette.io/) - ASGI framework
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- Pure HTML/CSS/JavaScript - No frontend frameworks

**Version:** 2.0  
**Last Updated:** January 28, 2026
