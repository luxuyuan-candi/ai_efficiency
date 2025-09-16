import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

DEEPSEEK_API_KEY = "sk-5c96f4b3f885469eb9af52bab183d654"
MCP_CPU_URL = "http://127.0.0.1:10001/mcp"
MCP_MEM_URL = "http://127.0.0.1:10002/mcp"
llm = ChatOpenAI(
    model = 'deepseek-chat',
    temperature=0.8,
    base_url = 'https://api.deepseek.com',
    api_key = DEEPSEEK_API_KEY,
)

async def main():
    # 配置系统提示词
    custom_prompt = """
你是一个运维小助手.
根据用户提出的问题，结合可以使用的工具，回答问题.
回答的内容的样式如下，其中"返回的结果"保持原始内容，并使用markdown格式：
<u>**查询的子对象**</u>
**返回的结果**
**分析的结论**
---
<u>**查询的子对象**</u>
**返回的结果**
**分析的结论**
---
...
---
**最终总结**
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
    })
    # 从这些 MCP servers 拿到 tools 列表
    tools = await client.get_tools()
    memory = MemorySaver()
    # 创建一个 Agent，用这些工具
    agent = create_react_agent(
        model=llm,  
        tools=tools,
        checkpointer=memory,
        prompt=custom_prompt
    )

    # 用 Agent 做一次调用
    config = {"configurable": {"thread_id": "2"}}
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "检查集群的整体情况"}]},
        config
    )

    print(response["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())
