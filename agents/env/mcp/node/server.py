from fastmcp import FastMCP
import os

mcp = FastMCP("mcp_kubectl_node")

@mcp.tool()
def command_kubectl_node() -> str:
    """
    用于查询项目集群对象的节点情况
    :return: 最终获得的答案
    """
    command_str = "kubectl get node"
    with os.popen(command_str) as f:
        output = f.read()
    return output

if __name__ == "__main__":
    print("Starting MCP HTTP server...")
    mcp.run(transport="http", host="0.0.0.0", port=10004)
