from fastmcp import FastMCP
import os

mcp = FastMCP("mcp_cpu")

@mcp.tool()
def command_uptime() -> str:
    """
    用于查询整个集群节点的cpu负载
    :return: 最终获得的答案
    """
    command_str = "uptime"
    with os.popen(command_str) as f:
        output = f.read()
    return output

if __name__ == "__main__":
    print("Starting MCP HTTP server...")
    mcp.run(transport="http", host="0.0.0.0", port=10001)
