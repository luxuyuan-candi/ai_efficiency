import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

DEEPSEEK_API_KEY = "sk-5c96f4b3f885469eb9af52bab183d654"
MCP_CPU_URL = "http://127.0.0.1:10001/mcp"

llm = ChatOpenAI(
    model = 'deepseek-chat',
    temperature=0.8,
    base_url = 'https://api.deepseek.com',
    api_key = DEEPSEEK_API_KEY,
)

async def main():
    # 配置 MCP servers
    client = MultiServerMCPClient({
        "mcp_cpu": {
            "url": MCP_CPU_URL,
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
        checkpointer=memory
    )

    # 用 Agent 做一次调用
    config = {"configurable": {"thread_id": "1"}}
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "cpu的负载是多少"}]},
        config
    )

    print(response["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())
