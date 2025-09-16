from fastmcp import FastMCP
import os

mcp = FastMCP("mcp_disk")

@mcp.tool()
def command_df() -> str:
    """
    用于查询项目集群基本资源的磁盘情况
    :return: 最终获得的答案
    """
    command_str = "df -h | egrep '^Filesystem|/$|/data$'"
    with os.popen(command_str) as f:
        output = f.read()
    return output

if __name__ == "__main__":
    print("Starting MCP HTTP server...")
    mcp.run(transport="http", host="0.0.0.0", port=10003)
