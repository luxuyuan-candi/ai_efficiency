from fastmcp import FastMCP
import os

mcp = FastMCP("mcp_kubectl_kafka")

@mcp.tool()
def command_kubectl_kafka() -> str:
    """
    用于查询项目集群中间件的kafka情况
    :return: 最终获得的答案
    """
    command_str = "kubectl get pod -A | grep kafka"
    with os.popen(command_str) as f:
        output = f.read()
    return output

if __name__ == "__main__":
    print("Starting MCP HTTP server...")
    mcp.run(transport="http", host="0.0.0.0", port=10007)
