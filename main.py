import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

#QWEN_API_KEY = "sk-4220a5ceb5f8427b98e3cc9ff6cddb76"
DEEPSEEK_API_KEY = "sk-5c96f4b3f885469eb9af52bab183d654"

MCP_CPU_URL = "http://127.0.0.1:10001/mcp"
MCP_MEM_URL = "http://127.0.0.1:10002/mcp"
MCP_DISK_URL = "http://127.0.0.1:10003/mcp"
MCP_KUBECTL_NODE_URL = "http://127.0.0.1:10004/mcp"

llm = ChatOpenAI(
    model = 'deepseek-chat',
    temperature=0.8,
    base_url = 'https://api.deepseek.com',
    api_key = DEEPSEEK_API_KEY,
)
#llm = ChatOpenAI(
#    model = 'qwen-plus',
#    temperature=0.8,
#    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1',
#    api_key = QWEN_API_KEY,
#)

async def main():
    # 配置系统提示词
    custom_prompt = """
你是一个运维小助手.
根据用户提出的问题，尽量使用的工具，回答问题.
<<内容要求
-"返回的结果"：保持原始内容。
-"项目基本情况"：不超过5个字。
/内容要求>>
回答的内容的样式如下，并使用markdown格式：
### 一、项目基本情况
{项目信息}
### 二、项目集群状态
#### {查询的子对象1}
**返回的结果**
```
{原始内容}
```
**分析的结论**
{结论}

---
#### {查询的子对象2}
**返回的结果**
```
{原始内容}
```
**分析的结论**
{结论}

---
...

---
#### {查询的子对象n}
**返回的结果**
```
{原始内容}
```
**分析的结论**
{结论}

---
#### 最终总结
### 三、项目业务情况
{项目业务}
"""
    # 配置 MCP servers
    client = MultiServerMCPClient({
        "mcp_cpu": {
            "url": MCP_CPU_URL,
            "transport": "streamable_http"
        },
        "mcp_mem": {
            "url": MCP_MEM_URL,
            "transport": "streamable_http"
        },
        "mcp_disk": {
            "url": MCP_DISK_URL,
            "transport": "streamable_http"
        },
        "mcp_kubectl_node": {
            "url": MCP_KUBECTL_NODE_URL,
            "transport": "streamable_http"
        },
        "mcp_kubectl_pod": {
            "url": "http://127.0.0.1:10005/mcp",
            "transport": "streamable_http"
        },
        "mcp_time": {
            "url": "http://127.0.0.1:10006/mcp",
            "transport": "streamable_http"
        },
        "mcp_kubectl_kafka": {
            "url": "http://127.0.0.1:10007/mcp",
            "transport": "streamable_http"
        },
        "mcp_kubectl_zookeeper": {
            "url": "http://127.0.0.1:10008/mcp",
            "transport": "streamable_http"
        },
        "mcp_kubectl_mysql": {
            "url": "http://127.0.0.1:10009/mcp",
            "transport": "streamable_http"
        },
        "mcp_kubectl_redis": {
            "url": "http://127.0.0.1:10010/mcp",
            "transport": "streamable_http"
        },
        "mcp_glusterd": {
            "url": "http://127.0.0.1:10011/mcp",
            "transport": "streamable_http"
        },
        "mcp_kubectl_mongodb": {
            "url": "http://127.0.0.1:10012/mcp",
            "transport": "streamable_http"
        },
    })
    # 从这些 MCP servers 拿到 tools 列表
    tools = await client.get_tools()
    #memory = MemorySaver()
    # 创建一个 Agent，用这些工具
    agent = create_react_agent(
        model=llm,  
        tools=tools,
        #checkpointer=memory,
        prompt=custom_prompt
    )

    # 用 Agent 做一次调用
    #config = {"configurable": {"thread_id": "2"}}
    info_project = "一见视觉平台是一款好的产品，需要查询相关文档"
    case_project = "项目业务情况良好，需要查询相关数据库"
    response = await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": "项目信息为:"+info_project},
            {"role": "user", "content": "项目业务为:"+case_project},
            {"role": "user", "content": "检查该项目"}
            ]},
        #config
    )

    print(response["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())
