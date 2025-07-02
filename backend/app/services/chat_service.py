from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List
from app.config import settings
import json

class GraphState(TypedDict):
    messages: List[dict]
    response: str

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-4o-mini",
            streaming=True
        )
        self.graph = self._create_graph()
    
    def _create_graph(self):
        def chat_node(state: GraphState):
            messages = [HumanMessage(content=msg["content"]) for msg in state["messages"] if msg["role"] == "user"]
            response = self.llm.invoke(messages)
            return {"response": response.content}
        
        workflow = StateGraph(GraphState)
        workflow.add_node("chat", chat_node)
        workflow.set_entry_point("chat")
        workflow.add_edge("chat", END)
        
        return workflow.compile()
    
    async def chat_stream(self, message: str):
        # Use LangGraph for streaming
        state = {"messages": [{"role": "user", "content": message}], "response": ""}
        
        # For streaming, we still need to call LLM directly since LangGraph doesn't stream yet
        messages = [HumanMessage(content=message)]
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                yield chunk.content
    
    async def chat(self, message: str) -> str:
        # Use LangGraph for non-streaming
        state = {"messages": [{"role": "user", "content": message}], "response": ""}
        result = await self.graph.ainvoke(state)
        return result["response"]
